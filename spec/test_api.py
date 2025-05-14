import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..database import Base, get_db
from ..seed import seed_database


# --- IN MEMORY SQLITE TEST DATABASE ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency to use test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- FIXTURES FOR HAPPY AND SAD TESTS ---
# DB fixtures 
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_database(db, num_users=3, num_posts=5, num_comments=10)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

# user fixtures 
@pytest.fixture
def test_user():
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    response = client.post("/api/users/register", json=user_data)
    return response.json()

# authentication fixtures 
@pytest.fixture
def test_token(test_user):
    response = client.post("/api/users/login", data={"username": "testuser", "password": "testpassword"})
    return response.json()["access_token"]



# --- HAPPY TESTS ---
# user 
def test_happy_register_user():
    user_data = {"username": "newuser", "email": "new@example.com", "password": "newpassword"}
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "new@example.com"

def test_happy_login_user(test_user):
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/api/users/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# post
def test_happy_create_post(test_token):
    post_data = {"title": "Test Post", "content": "This is a test post"}
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/posts/", json=post_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
    assert response.json()["content"] == "This is a test post"

def test_happy_browse_posts():
    response = client.get("/api/posts/")
    assert response.status_code == 200
    assert len(response.json()) >= 5
    assert all("title" in post for post in response.json())

def test_happy_search_posts():
    response = client.get("/api/posts/search?keyword=post")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any("post" in post["title"].lower() or "post" in post["content"].lower() for post in response.json())

# comment 
def test_happy_create_comment(test_token):
    response = client.get("/api/posts/")
    post_id = response.json()[0]["id"]
    comment_data = {"content": "This is a test comment"}
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post(f"/api/comments/{post_id}", json=comment_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["content"] == "This is a test comment"
    assert response.json()["post_id"] == post_id

def test_happy_get_comments():
    response = client.get("/api/posts/")
    post_id = response.json()[0]["id"]
    response = client.get(f"/api/comments/{post_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert all("content" in comment for comment in response.json())

# settings 
def test_happy_get_settings(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/settings/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json()["dark_mode"], bool)
    assert "display_username" in response.json()

def test_happy_update_settings(test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    setting_data = {"display_username": "CoolUser", "dark_mode": True}
    response = client.put("/api/settings/", json=setting_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["display_username"] == "CoolUser"
    assert response.json()["dark_mode"] is True

# --- SAD TESTS ---
# user 
def test_sad_register_duplicate_username(test_user):
    user_data = {"username": "testuser", "email": "another@example.com", "password": "testpassword"}
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_sad_login_invalid_credentials():
    login_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/api/users/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

# post 
def test_sad_create_post_unauthenticated():
    post_data = {"title": "Test Post", "content": "This is a test post"}
    response = client.post("/api/posts/", json=post_data)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

# comment 
def test_sad_create_comment_invalid_post_id(test_token):
    comment_data = {"content": "This is a test comment"}
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/comments/999", json=comment_data, headers=headers)
    assert response.status_code == 404
    assert "Post not found" in response.json()["detail"]

def test_sad_get_comments_invalid_post_id():
    response = client.get("/api/comments/999")
    assert response.status_code == 404
    assert "Post not found" in response.json()["detail"]

# setting 
def test_sad_update_settings_unauthenticated():
    setting_data = {"display_username": "CoolUser", "dark_mode": True}
    response = client.put("/api/settings/", json=setting_data)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]