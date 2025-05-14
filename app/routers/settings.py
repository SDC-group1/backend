from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, auth

router = APIRouter()

@router.get("/", response_model=schemas.UserSettingResponse)
def get_settings(
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    settings = crud.get_user_setting(db, current_user.id)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

@router.put("/", response_model=schemas.UserSettingResponse)
def update_settings(
    setting: schemas.UserSettingCreate,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    settings = crud.update_user_setting(db, current_user.id, setting)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings