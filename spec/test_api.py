import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app, fake_blogs_db

client = TestClient(app)

# Fixture to reset the fake_blogs_db before each test
@pytest.fixture(autouse=True)
def reset_db():
    fake_blogs_db.clear()
    fake_blogs_db.extend([
        {"id": 0, "name": "Understanding FastAPI"},
        {"id": 1, "name": "Deploying Python Apps with Docker"},
        {"id": 2, "name": "Async IO in Python: A Practical Guide"}
    ])

# HAPPY Path Tests
def test_happy_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Blog API"}

def test_happy_read_blogs():
    response = client.get("/blogs/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 0, "name": "Understanding FastAPI"},
        {"id": 1, "name": "Deploying Python Apps with Docker"},
        {"id": 2, "name": "Async IO in Python: A Practical Guide"}
    ]

def test_happy_read_blog():
    response = client.get("/blogs/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Deploying Python Apps with Docker"}

def test_happy_create_blog():
    new_blog = {"name": "New Blog Post"}
    response = client.post("/blogs/", json=new_blog)
    assert response.status_code == 200
    assert response.json() == {"id": 3, "name": "New Blog Post"}
    assert fake_blogs_db[-1] == {"id": 3, "name": "New Blog Post"}

# SAD Path Tests
def test_sad_read_blog_invalid_id():
    response = client.get("/blogs/999")
    assert response.status_code == 404  

def test_sad_create_blog_missing_name():
    response = client.post("/blogs/", json={})
    assert response.status_code == 422  # FastAPI automatically validates Pydantic models

def test_sad_create_blog_invalid_data():
    response = client.post("/blogs/", json={"name": ""})
    assert response.status_code == 422  # Pydantic validation for non-empty string