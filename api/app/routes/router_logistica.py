from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_session
from app.models import Logistica
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[Logistica])
def get_logistica(
    estado_envio: Optional[str] = None,  
    proveedor_id: Optional[str] = None, 
    fecha_inicio: Optional[str] = None, 
    fecha_fin: Optional[str] = None,
    limit: int = 1000,
    offset: int = 0,
    session: Session = Depends(get_session)
):
    query = session.query(Logistica)

    if estado_envio:
        query = query.filter(Logistica.estado_envio == estado_envio)
    
    if proveedor_id:
        query = query.filter(Logistica.proveedor_id == proveedor_id)

    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(Logistica.fecha_envio >= fecha_inicio)
        except ValueError:
            raise ValueError("La fecha de inicio debe tener el formato YYYY-MM-DD.")
    
    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Logistica.fecha_envio <= fecha_fin)
        except ValueError:
            raise ValueError("La fecha de fin debe tener el formato YYYY-MM-DD.")
    
    return query.offset(offset).limit(limit).all()