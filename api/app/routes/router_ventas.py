from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db import get_session
from app.models import Ventas, Clientes, Productos
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[Ventas])
def get_ventas(
    genero_cliente: Optional[str] = None, 
    edad_cliente: Optional[int] = None,   
    sucursal_id: Optional[int] = None,   
    producto_id: Optional[str] = None,    
    fecha_inicio: Optional[str] = None,   
    fecha_fin: Optional[str] = None,
    limit: int = 1000,
    offset: int = 0,    
    session: Session = Depends(get_session)
):
    query = session.query(Ventas)
    
    query = query.join(Clientes, Clientes.cliente_id == Ventas.cliente_id)

    query = query.options(
        joinedload(Ventas.cliente),
        joinedload(Ventas.producto)
    )
    
    if genero_cliente:
        query = query.filter(Clientes.genero == genero_cliente)
    
    if edad_cliente:
        query = query.filter(Clientes.edad == edad_cliente)
    
    if sucursal_id:
        query = query.filter(Ventas.sucursal_id == sucursal_id)
    
    if producto_id:
        query = query.filter(Ventas.producto_id == producto_id)

    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(Ventas.fecha >= fecha_inicio)
        except ValueError:
            raise ValueError("La fecha de inicio debe tener el formato YYYY-MM-DD.")
    
    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Ventas.fecha <= fecha_fin)
        except ValueError:
            raise ValueError("La fecha de fin debe tener el formato YYYY-MM-DD.")
    
    return query.offset(offset).limit(limit).all()