from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# class CommentCreate(BaseModel):
#     content: str

# class CommentResponse(BaseModel):
#     id: int
#     content: str
#     post_id: int
#     author_id: int
#     created_at: datetime

#     class Config:
#         from_attributes = True

# class UserSettingCreate(BaseModel):
#     display_username: Optional[str] = None
#     dark_mode: bool = False

# class UserSettingResponse(BaseModel):
#     id: int
#     user_id: int
#     display_username: Optional[str]
#     dark_mode: bool

#     class Config:
#         from_attributes = True