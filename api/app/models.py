from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import date

class Productos(SQLModel, table=True):
    producto_id: str = Field(primary_key=True, max_length=10)
    nombre_producto: str
    categoria: str
    precio_base: float

    ventas: List["Ventas"] = Relationship(back_populates="producto")

class Clientes(SQLModel, table=True):
    cliente_id: str = Field(primary_key=True, max_length=10)
    nombre: str
    edad: Optional[int] = None
    genero: str = Field(max_length=50)
    ubicacion: Optional[str] = None

    ventas: List["Ventas"] = Relationship(back_populates="cliente")

class Proveedores(SQLModel, table=True):
    proveedor_id: str = Field(primary_key=True, max_length=10)
    nombre_proveedor: str
    contacto: Optional[str] = None
    ubicacion: Optional[str] = None

    logistica: List["Logistica"] = Relationship(back_populates="proveedor")

class Ventas(SQLModel, table=True):
    venta_id: str = Field(primary_key=True, max_length=10)
    producto_id: str = Field(foreign_key="productos.producto_id")
    cantidad: int
    precio_unitario: float
    cliente_id: str = Field(foreign_key="clientes.cliente_id")
    sucursal_id: Optional[int] = None
    total: float
    fecha: Optional[date] = None

    producto: Optional[Productos] = Relationship(back_populates="ventas")
    cliente: Optional[Clientes] = Relationship(back_populates="ventas")
    logistica: List["Logistica"] = Relationship(back_populates="venta")

class Logistica(SQLModel, table=True):
    envio_id: str = Field(primary_key=True, max_length=10)
    venta_id: str = Field(foreign_key="ventas.venta_id")
    proveedor_id: str = Field(foreign_key="proveedores.proveedor_id")
    estado_envio: str
    fecha_envio: Optional[date] = None

    venta: Optional[Ventas] = Relationship(back_populates="logistica")
    proveedor: Optional[Proveedores] = Relationship(back_populates="logistica")
