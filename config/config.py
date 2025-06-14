from fastapi import HTTPException, status
import firebase_admin
from dotenv import load_dotenv
import pathlib

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token

from db import SessionLocal

bearer_scheme = HTTPBearer(auto_error=False)

basedir = pathlib.Path(__file__).parents[0]

load_dotenv(basedir / ".env")

def initialize_firebase():
    if not firebase_admin._apps:
        # Initialize Firebase only if it hasn't been initialized yet
        firebase_admin.initialize_app()

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()