from fastapi import FastAPI, HTTPException, status, Body
from routes.saludos import router as saludos
from routes.usuaris import router as usuaris
from fastapi.middleware.cors import CORSMiddleware
import os
import firebase_admin
from dotenv import load_dotenv
import pathlib

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token

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

basedir = pathlib.Path(__file__).parents[0]

print("basedir", basedir)

load_dotenv(basedir / ".env")

app = FastAPI()

print("url", os.getenv("FRONTEND_URL", ""))

origins = [os.getenv("FRONTEND_URL", "")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebase_admin.initialize_app()

app.include_router(saludos)
app.include_router(usuaris)

@app.get("/userid")
async def get_userid(auth: Annotated[dict, Depends(get_firebase_user_from_token)]):
    """gets the firebase connected user"""
    return {"id": auth["uid"]}
