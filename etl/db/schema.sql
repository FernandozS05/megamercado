CREATE TABLE proveedores (
    proveedor_id VARCHAR(10) PRIMARY KEY,
    nombre_proveedor VARCHAR(255),
    contacto VARCHAR(255),
    ubicacion VARCHAR(255)
);

CREATE INDEX idx_proveedores_ubicacion ON proveedores(ubicacion);
CREATE INDEX idx_proveedores_nombre ON proveedores(nombre_proveedor);

CREATE TABLE clientes (
    cliente_id VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(255),
    edad INT,
    genero VARCHAR(50) CHECK (genero IN ('Masculino', 'Femenino', 'Otro')),
    ubicacion VARCHAR(255)
);

CREATE INDEX idx_clientes_ubicacion ON clientes(ubicacion);
CREATE INDEX idx_clientes_nombre ON clientes(nombre);

CREATE TABLE productos (
    producto_id VARCHAR(10) PRIMARY KEY,
    nombre_producto VARCHAR(255),
    categoria VARCHAR(100) CHECK (categoria IN ('Abarrotes', 'Electrónica', 'Ropa', 'Hogar', 'Salud')),
    precio_base DECIMAL(10,2)
);

CREATE INDEX idx_productos_categoria ON productos(categoria);
CREATE INDEX idx_productos_precio_base ON productos(precio_base);

CREATE TABLE ventas (
    venta_id VARCHAR(10) PRIMARY KEY,
    producto_id VARCHAR(10) REFERENCES productos (producto_id),
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    cliente_id VARCHAR(10) REFERENCES clientes (cliente_id),
    sucursal_id VARCHAR(10),
    total DECIMAL(10,2),
    fecha DATE
);

CREATE INDEX idx_ventas_producto_id ON ventas(producto_id);
CREATE INDEX idx_ventas_cliente_id ON ventas(cliente_id);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);
CREATE INDEX idx_ventas_sucursal_id ON ventas(sucursal_id);

CREATE TABLE logistica (
    envio_id VARCHAR(10) PRIMARY KEY,
    venta_id VARCHAR(10) REFERENCES ventas (venta_id),
    proveedor_id VARCHAR(10) REFERENCES proveedores (proveedor_id),
    fecha_envio DATE,
    estado_envio VARCHAR(50) CHECK (estado_envio IN ('Retrasado', 'Entregado', 'En tránsito', 'Cancelado'))
);

CREATE INDEX idx_logistica_venta_id ON logistica(venta_id);
CREATE INDEX idx_logistica_proveedor_id ON logistica(proveedor_id);
CREATE INDEX idx_logistica_fecha_envio ON logistica(fecha_envio);
CREATE INDEX idx_logistica_estado_envio ON logistica(estado_envio);
CREATE INDEX idx_ventas_fecha_cliente_id ON ventas(fecha, cliente_id);
CREATE INDEX idx_logistica_fecha_proveedor ON logistica(fecha_envio, proveedor_id);
