from fastapi import FastAPI
from config.config import initialize_firebase
from routes.saludos import router as saludos
from routes.usuaris import router as usuaris
from routes.pedidos import router as pedidos
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

initialize_firebase()

origins = [os.getenv("FRONTEND_URL", ""), "https://v0-new-project-5yx1vjjggmb-iz4ovmt59-rahms-projects-5ef39cf9.vercel.app/home"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(saludos)
app.include_router(usuaris)
app.include_router(pedidos)
