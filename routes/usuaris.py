from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from config.config import get_firebase_user_from_token, get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status

from models.models import Usuaris

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

di_auth = Annotated[dict, Depends(get_firebase_user_from_token)]
di_db = Annotated[Session, Depends(get_db)]

class UserRequest(BaseModel):
    US_Id: int | None = Field(None, ge=0, le=999999999)
    US_Id_Session: str = Field(..., min_length=1, max_length=100)
    US_Nom: str = Field(..., min_length=0, max_length=50)
    US_Cognoms: str = Field(..., min_length=0, max_length=50)
    US_Email: str = Field(..., min_length=1, max_length=100)
    US_Status: bool = True

@router.get("/", status_code=status.HTTP_200_OK)
def select_users(auth: di_auth, db: di_db):
    users = db.query(Usuaris).filter(Usuaris.US_Status == 1).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(auth: di_auth, db: di_db, user: UserRequest):
    new_user = Usuaris(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/", status_code=status.HTTP_201_CREATED)
def update_user(auth: di_auth, db: di_db, user: UserRequest):
    existing_user = db.query(Usuaris).filter(Usuaris.US_Id == user.US_Id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user.model_dump().items():
        setattr(existing_user, key, value)
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    return existing_user

@router.delete("/{user_id}", status_code=status.HTTP_201_CREATED)
def delete_user(auth: di_auth, db: di_db, user_id: int):
    existing_user = db.query(Usuaris).filter(Usuaris.US_Id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    setattr(existing_user, "US_Status", False)
    db.add(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def select_user(auth: di_auth, db: di_db, user_id: int):
    user = db.query(Usuaris).filter(Usuaris.US_Id == user_id, Usuaris.US_Status == 1).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/selectbyparams")
def select_by_parameters(auth: di_auth, db: di_db, id: int):
    user = db.query(Usuaris).filter(Usuaris.US_Id == id, Usuaris.US_Status == 1).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
