from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_session
from app.models import Clientes

router = APIRouter()

@router.get("/", response_model=List[Clientes])
def get_clientes(
    cliente_id: Optional[str] = None,
    nombre: Optional[str] = None,
    genero: Optional[str] = None,
    ubicacion: Optional[str] = None,
    edad: Optional[int] = None,
    limit: int = 1000,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    query = session.query(Clientes)
    
    if cliente_id:
        query = query.filter(Clientes.cliente_id == cliente_id)
    
    if nombre:
        query = query.filter(Clientes.nombre == nombre)
    
    if genero:
        query = query.filter(Clientes.genero == genero)
    
    if ubicacion:
        query = query.filter(Clientes.ubicacion == ubicacion)
    
    if edad:
        query = query.filter(Clientes.edad == edad)
    
    return query.offset(offset).limit(limit).all()
