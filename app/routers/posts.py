from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ... import schemas, database, crud, auth
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    return crud.create_post(db, post, current_user.id)

@router.get("/", response_model=List[schemas.PostResponse])
def browse_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db)
):
    return crud.get_posts(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[schemas.PostResponse])
def search_posts(
    keyword: str = Query(...),
    db: Session = Depends(database.get_db)
):
    return crud.search_posts(db, keyword)