from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_session
from app.models import Proveedores

router = APIRouter()

@router.get("/", response_model=List[Proveedores])
def get_proveedores(
    proveedor_id: Optional[str] = None, 
    nombre_proveedor: Optional[str] = None,
    contacto: Optional[str] = None,
    ubicacion: Optional[str] = None,
    limit: int = 1000,
    offset: int = 0, 
    session: Session = Depends(get_session)
):
    query = session.query(Proveedores)
    
    if proveedor_id:
        query = query.filter(Proveedores.proveedor_id == proveedor_id)
    
    if nombre_proveedor:
        query = query.filter(Proveedores.nombre_proveedor == nombre_proveedor)
    
    if contacto:
        query = query.filter(Proveedores.contacto == contacto)

    if ubicacion:
        query = query.filter(Proveedores.ubicacion == ubicacion)
    
    return query.offset(offset).limit(limit).all()