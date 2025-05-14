from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from sqlalchemy import or_

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Create default settings
    db_setting = models.UserSetting(user_id=db_user.id)
    db.add(db_setting)
    db.commit()
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def search_posts(db: Session, keyword: str):
    return db.query(models.Post).filter(
        or_(
            models.Post.title.ilike(f"%{keyword}%"),
            models.Post.content.ilike(f"%{keyword}%")
        )
    ).all()

def create_comment(db: Session, comment: schemas.CommentCreate, post_id: int, user_id: int):
    db_comment = models.Comment(**comment.dict(), post_id=post_id, author_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db: Session, post_id: int):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

def get_user_setting(db: Session, user_id: int):
    return db.query(models.UserSetting).filter(models.UserSetting.user_id == user_id).first()

def update_user_setting(db: Session, user_id: int, setting: schemas.UserSettingCreate):
    db_setting = db.query(models.UserSetting).filter(models.UserSetting.user_id == user_id).first()
    if db_setting:
        for key, value in setting.dict(exclude_unset=True).items():
            setattr(db_setting, key, value)
        db.commit()
        db.refresh(db_setting)
    return db_setting