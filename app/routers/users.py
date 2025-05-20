from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, crud, auth

router = APIRouter()

# @router.post("/register", response_model=schemas.UserResponse)
# def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
#     db_user = crud.get_user_by_username(db, user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     db_user = crud.get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db, user)

# @router.post("/login", response_model=schemas.Token)
# def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     user = crud.get_user_by_username(db, form_data.username)
#     if not user or not crud.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = auth.create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}