import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_data(endpoint: str, params: dict = None):
    response = requests.get(f"{API_URL}/{endpoint}", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener datos: {response.status_code}")
        return []

def remove_empty_params(params):
    return {k: v for k, v in params.items() if v not in [None, "", 0]}

st.title("Dashboard de datos")

st.header("Consultar todas las tablas")

pagina = st.number_input("Página", min_value=1, value=1, step=1)
registros_por_pagina = 1000
offset = (pagina - 1) * registros_por_pagina
pagination_params = {"limit": registros_por_pagina, "offset": offset}

if st.button("Cargar Productos"):
    productos = get_data("productos", params=pagination_params)
    st.write(pd.DataFrame(productos))

if st.button("Cargar Clientes"):
    clientes = get_data("clientes", params=pagination_params)
    st.write(pd.DataFrame(clientes))

if st.button("Cargar Proveedores"):
    proveedores = get_data("proveedores", params=pagination_params)
    st.write(pd.DataFrame(proveedores))

if st.button("Cargar Ventas"):
    ventas = get_data("ventas", params=pagination_params)
    st.write(pd.DataFrame(ventas))

if st.button("Cargar Logística"):
    logistica = get_data("logistica", params=pagination_params)
    st.write(pd.DataFrame(logistica))

st.header("Realizar consultas con filtros")

st.subheader("Consultar Productos")
nombre_producto = st.text_input("Nombre del Producto", key="nombre_producto")
categoria_producto = st.selectbox("Categoría", ["", "Abarrotes", "Electrónica", "Ropa", "Hogar", "Salud"], key="categoria_producto")
precio_min = st.number_input("Precio Mínimo", min_value=0.0, key="precio_min")
precio_max = st.number_input("Precio Máximo", min_value=0.0, key="precio_max")
producto_id = st.text_input("ID Producto", key="producto_id")

if st.button("Consultar Productos con Filtros"):
    params = remove_empty_params({
        "nombre_producto": nombre_producto,
        "categoria": categoria_producto,
        "precio_min": precio_min,
        "precio_max": precio_max,
        "producto_id": producto_id,
        **pagination_params
    })
    productos_filtrados = get_data("productos", params=params)
    st.write(pd.DataFrame(productos_filtrados))

st.subheader("Consultar Clientes")
cliente_id = st.text_input("ID del Cliente", key="cliente_id")
nombre_cliente = st.text_input("Nombre del Cliente", key="nombre_cliente")
genero_cliente = st.selectbox("Género", ["", "Masculino", "Femenino", "Otro"], key="genero_cliente")
ubicacion_cliente = st.text_input("Ubicación", key="ubicacion_cliente")
edad_cliente = st.number_input("Edad", min_value=0, key="edad_cliente")

if st.button("Consultar Clientes con Filtros"):
    params = remove_empty_params({
        "cliente_id": cliente_id,
        "nombre": nombre_cliente,
        "genero": genero_cliente,
        "ubicacion": ubicacion_cliente,
        "edad": edad_cliente,
        **pagination_params
    })
    clientes_filtrados = get_data("clientes", params=params)
    st.write(pd.DataFrame(clientes_filtrados))

st.subheader("Consultar Proveedores")
proveedor_id = st.text_input("ID del Proveedor", key="proveedor_id")
nombre_proveedor = st.text_input("Nombre del Proveedor", key="nombre_proveedor")
contacto_proveedor = st.text_input("Contacto (Correo)", key="contacto_proveedor")
ubicacion_proveedor = st.text_input("Ubicación", key="ubicacion_proveedor")

if st.button("Consultar Proveedores con Filtros"):
    params = remove_empty_params({
        "proveedor_id": proveedor_id,
        "nombre_proveedor": nombre_proveedor,
        "contacto": contacto_proveedor,
        "ubicacion": ubicacion_proveedor,
        **pagination_params
    })
    proveedores_filtrados = get_data("proveedores", params=params)
    st.write(pd.DataFrame(proveedores_filtrados))

st.subheader("Consultar Ventas")
genero_cliente_ventas = st.selectbox("Género Cliente", ["", "Masculino", "Femenino", "Otro"], key="genero_cliente_ventas")
edad_cliente_ventas = st.number_input("Edad Cliente", min_value=0, key="edad_cliente_ventas")
sucursal_id_ventas = st.number_input("ID Sucursal", min_value=0, step=1, key="sucursal_id_ventas")
producto_id_ventas = st.text_input("ID Producto", key="producto_id_ventas")
fecha_inicio_ventas = st.date_input("Fecha de Inicio", key="fecha_inicio_ventas")
fecha_fin_ventas = st.date_input("Fecha de Fin", key="fecha_fin_ventas")

if st.button("Consultar Ventas con Filtros"):
    params = remove_empty_params({
        "genero_cliente": genero_cliente_ventas,
        "edad_cliente": edad_cliente_ventas,
        "sucursal_id": sucursal_id_ventas,
        "producto_id": producto_id_ventas,
        "fecha_inicio": fecha_inicio_ventas,
        "fecha_fin": fecha_fin_ventas,
        **pagination_params
    })
    ventas_filtradas = get_data("ventas", params=params)
    st.write(pd.DataFrame(ventas_filtradas))

st.subheader("Consultar Logística")
estado_envio = st.selectbox("Estado de Envío", ["", "Retrasado", "Entregado", "En tránsito", "Cancelado"], key="estado_envio")
proveedor_id_logistica = st.text_input("Proveedor ID", key="proveedor_id_logistica")
fecha_inicio_logistica = st.date_input("Fecha de Inicio", key="fecha_inicio_logistica")
fecha_fin_logistica = st.date_input("Fecha de Fin", key="fecha_fin_logistica")

if st.button("Consultar Logística con Filtros"):
    params = remove_empty_params({
        "estado_envio": estado_envio,
        "proveedor_id": proveedor_id_logistica,
        "fecha_inicio": fecha_inicio_logistica,
        "fecha_fin": fecha_fin_logistica,
        **pagination_params
    })
    logistica_filtrada = get_data("logistica", params=params)
    st.write(pd.DataFrame(logistica_filtrada))