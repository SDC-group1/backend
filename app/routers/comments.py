from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ... import schemas, database, crud, auth
from typing import List

router = APIRouter()

@router.post("/{post_id}", response_model=schemas.CommentResponse)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return crud.create_comment(db, comment, post_id, current_user.id)

@router.get("/{post_id}", response_model=List[schemas.CommentResponse])
def get_comments(
    post_id: int,
    db: Session = Depends(database.get_db)
):
    return crud.get_comments(db, post_id)