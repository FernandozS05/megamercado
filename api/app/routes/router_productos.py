from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_session
from app.models import Productos

router = APIRouter()

@router.get("/", response_model=List[Productos])
def get_productos(
    producto_id: Optional[str] = None,
    nombre_producto: Optional[str] = None,
    categoria: Optional[str] = None,
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None,
    session: Session = Depends(get_session)
):
    query = session.query(Productos)
    
    if producto_id:
        query = query.filter(Productos.producto_id == producto_id)
    
    if nombre_producto:
        query = query.filter(Productos.nombre_producto == nombre_producto)
    
    if categoria:
        query = query.filter(Productos.categoria == categoria)
    
    if precio_min:
        query = query.filter(Productos.precio_base >= precio_min)

    if precio_max:
        query = query.filter(Productos.precio_base <= precio_max)
    
    return query.all()
