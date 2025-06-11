from fastapi import APIRouter, FastAPI, HTTPException, status, Body
from dotenv import load_dotenv
from pydantic import BaseModel
from db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token

from models.models import Usuaris

bearer_scheme = HTTPBearer(auto_error=False)

def get_firebase_user_from_token(
    token: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> dict | None:
    try:
        if not token:
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

di_auth = Annotated[dict, Depends(get_firebase_user_from_token)]
di_db = Annotated[Session, Depends(get_db)]

class UserRequest(BaseModel):
    US_Id: int | None = None
    US_Nom: str
    US_Cognoms: str
    US_Email: str
    US_Status: bool = True

@router.get("/users", status_code=status.HTTP_200_OK)
def select_users(auth: di_auth, db: di_db):
    users = db.query(Usuaris).filter(Usuaris.US_Status == 1).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users

@router.post("/users/create", status_code=status.HTTP_201_CREATED)
def create_user(auth: di_auth, db: di_db, user: UserRequest):
    new_user = Usuaris(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/update", status_code=status.HTTP_201_CREATED)
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

@router.delete("/users/delete/{user_id}", status_code=status.HTTP_201_CREATED)
def delete_user(auth: di_auth, db: di_db, user_id: int):
    existing_user = db.query(Usuaris).filter(Usuaris.US_Id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    setattr(existing_user, "US_Status", False)
    db.add(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def select_user(auth: di_auth, db: di_db, user_id: int):
    user = db.query(Usuaris).filter(Usuaris.US_Id == user_id, Usuaris.US_Status == 1).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/selectbyparams/users")
def select_by_parameters(auth: di_auth, db: di_db, id: int):
    user = db.query(Usuaris).filter(Usuaris.US_Id == id, Usuaris.US_Status == 1).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
