from sqlalchemy.orm import Session
from faker import Faker
from . import models, crud, schemas
import random

fake = Faker()

def seed_database(db: Session, num_users=5, num_posts=10, num_comments=20):
    """
    Seed the database with fake users, posts, comments, and settings.
    
    Args:
        db: SQLAlchemy database session
        num_users: Number of fake users to create
        num_posts: Number of fake posts to create
        num_comments: Number of fake comments to create
    """
    # Create fake users
    users = []
    for _ in range(num_users):
        user_data = schemas.UserCreate(
            username=fake.user_name(),
            email=fake.email(),
            password="testpassword"  # Same password for simplicity
        )
        user = crud.create_user(db, user_data)
        users.append(user)

    # Create fake posts
    posts = []
    for _ in range(num_posts):
        post_data = schemas.PostCreate(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=5)
        )
        user = random.choice(users)
        post = crud.create_post(db, post_data, user.id)
        posts.append(post)

    # Create fake comments
    for _ in range(num_comments):
        comment_data = schemas.CommentCreate(
            content=fake.paragraph(nb_sentences=2)
        )
        user = random.choice(users)
        post = random.choice(posts)
        crud.create_comment(db, comment_data, post.id, user.id)

    # Update user settings
    for user in users:
        setting_data = schemas.UserSettingCreate(
            display_username=fake.name(),
            dark_mode=random.choice([True, False])
        )
        crud.update_user_setting(db, user.id, setting_data)

    print(f"Seeded {num_users} users, {num_posts} posts, {num_comments} comments")