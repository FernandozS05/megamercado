from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routes.router_productos import router as router_productos
from app.routes.router_clientes import router as router_clientes
from app.routes.router_proveedores import router as router_proveedores
from app.routes.router_ventas import router as router_ventas
from app.routes.router_logistica import router as router_logistica 

app = FastAPI()

app.include_router(router_productos, prefix="/productos", tags=["Productos"])
app.include_router(router_clientes, prefix="/clientes", tags=["Clientes"])
app.include_router(router_proveedores, prefix="/proveedores", tags=["Proveedores"])
app.include_router(router_ventas, prefix="/ventas", tags=["Ventas"])
app.include_router(router_logistica, prefix="/logistica", tags=["Logística"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()