import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

db_url = "postgresql://postgres:12345@localhost:5432/megamercado"
engine = create_engine(db_url)

st.title("Exploración de tendencias en las ventas")

ventas_totales = pd.read_sql("SELECT SUM(total) AS ventas_totales FROM ventas;", con=engine)
st.subheader("Ventas totales")
st.table(ventas_totales)

df_ingresos_sucursal = pd.read_sql("""
SELECT sucursal_id AS sucursal, SUM(total) AS ingresos_totales
FROM ventas 
GROUP BY sucursal
ORDER BY ingresos_totales DESC
LIMIT 10;
""", con=engine)

st.subheader("Sucursales con más ventas")
fig = px.bar(df_ingresos_sucursal, x="sucursal", y="ingresos_totales", 
             title="Sucursales con Más Ventas", labels={"sucursal": "Sucursal ID", "ingresos_totales": "Ingresos Totales"})
st.plotly_chart(fig)

df_ventas_categoria = pd.read_sql("""
SELECT p.categoria, SUM(v.total) AS ventas_categoria
FROM ventas v
JOIN productos p ON v.producto_id = p.producto_id
GROUP BY p.categoria
ORDER BY ventas_categoria DESC;
""", con=engine)

st.subheader("Ventas por categoría")
fig = px.bar(df_ventas_categoria, x="categoria", y="ventas_categoria", 
             title="Ventas por categoría", labels={"categoria": "Categoría", "ventas_categoria": "Total de Ventas"})
st.plotly_chart(fig)

df_ventas_genero = pd.read_sql("""
SELECT c.genero, SUM(v.total) AS ventas_genero
FROM ventas v
JOIN clientes c ON v.cliente_id = c.cliente_id
GROUP BY c.genero
ORDER BY ventas_genero DESC;
""", con=engine)

st.subheader("Ventas por género")
fig = px.pie(df_ventas_genero, names="genero", values="ventas_genero", title="Distribución de ventas por género")
st.plotly_chart(fig)
