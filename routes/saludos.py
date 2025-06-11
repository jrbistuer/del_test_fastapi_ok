from fastapi import APIRouter

router = APIRouter()

@router.get("/api/saludo")
async def root():
    return {"message": "Hola mundo!"}

@router.get("/api/saludo2")
async def saludo():
    return {"messages": "Hola, ¿cómo estás?"}