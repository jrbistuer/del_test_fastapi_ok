from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from config.config import get_firebase_user_from_token, get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends, HTTPException, status

from models.models import Pedidos

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
)

di_auth = Annotated[dict, Depends(get_firebase_user_from_token)]
di_db = Annotated[Session, Depends(get_db)]

class PedidosRequest(BaseModel):
    PED_Id: int | None = Field(None, ge=0, le=999999999)
    PED_Id_User: str = Field(..., min_length=1, max_length=100)
    PED_Nombre: str = Field(..., min_length=1, max_length=100)
    PED_Descripcion: str = Field(..., min_length=1, max_length=255)
    PED_Precio: int = Field(..., ge=0)

@router.get("/", status_code=status.HTTP_200_OK)
def select_pedidos(auth: di_auth, db: di_db):
    pedidos = db.query(Pedidos).filter(Pedidos.PED_Id_User == auth["user_id"]).all()
    if not pedidos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pedidos found")
    return pedidos

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pedido(auth: di_auth, db: di_db, pedido: PedidosRequest):
    new_pedido = Pedidos(**pedido.model_dump())
    new_pedido.PED_Id_User = auth["user_id"]
    db.add(new_pedido)
    db.commit()
    db.refresh(new_pedido)
    return new_pedido

@router.put("/", status_code=status.HTTP_201_CREATED)
def update_pedido(auth: di_auth, db: di_db, pedido: PedidosRequest):
    existing_pedido = db.query(Pedidos).filter(Pedidos.PED_Id == pedido.PED_Id).first()
    if not existing_pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found")
    for key, value in pedido.model_dump().items():
        setattr(existing_pedido, key, value)
    db.add(existing_pedido)
    db.commit()
    db.refresh(existing_pedido)
    return existing_pedido  

@router.delete("/{pedido_id}", status_code=status.HTTP_201_CREATED)
def delete_pedido(auth: di_auth, db: di_db, pedido_id: int):
    existing_pedido = db.query(Pedidos).filter(Pedidos.PED_Id == pedido_id and Pedidos.PED_Id_User == auth["user_id"]).first()
    if not existing_pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found")
    setattr(existing_pedido, "PED_Status", False)
    db.add(existing_pedido)
    db.commit()
    db.refresh(existing_pedido)
    return {"message": "Pedido deleted successfully"}

@router.get("/{pedido_id}", status_code=status.HTTP_200_OK)
def select_pedido(auth: di_auth, db: di_db, pedido_id: int):
    pedido = db.query(Pedidos).filter(Pedidos.PED_Id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found")
    return pedido
