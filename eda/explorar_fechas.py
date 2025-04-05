import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

db_url = "postgresql://postgres:12345@localhost:5432/megamercado"
engine = create_engine(db_url)

st.title("Exploración de las ventas y envíos (logística) por intervalo de fechas")

df_ventas_anio = pd.read_sql("""
SELECT EXTRACT(YEAR FROM fecha) AS anio, COUNT(*) AS total_ventas
FROM ventas
GROUP BY anio
ORDER BY anio;
""", con=engine)

df_ventas_anio['anio'] = df_ventas_anio['anio'].astype(int)
df_ventas_anio.rename(columns={"anio": "año"}, inplace=True)

st.subheader("Distribución de ventas por año")
st.write(df_ventas_anio)

fig = px.bar(df_ventas_anio, 
             x=df_ventas_anio["año"].astype(str),
             y="total_ventas", 
             title="Distribución de ventas por año", 
             labels={"año": "Año"})

fig.update_layout(
    xaxis_title="Año",
    xaxis=dict(type="category", categoryorder="category ascending") 
)

st.plotly_chart(fig)

df_ventas_mes = pd.read_sql("""
SELECT TO_CHAR(fecha, 'Month') AS mes_nombre, COUNT(*) AS total_ventas
FROM ventas
GROUP BY mes_nombre
ORDER BY total_ventas DESC;
""", con=engine)

st.subheader("Distribución de ventas por mes")
st.write(df_ventas_mes)
fig = px.bar(df_ventas_mes, x="mes_nombre", y="total_ventas", title="Distribución de ventas por mes")
st.plotly_chart(fig)

df_ventas_dia = pd.read_sql("""
SELECT TO_CHAR(fecha, 'Day') AS dia_nombre, COUNT(*) AS total_ventas
FROM ventas
GROUP BY dia_nombre
ORDER BY total_ventas DESC;
""", con=engine)

st.subheader("Distribución de ventas por día de la semana")
st.write(df_ventas_dia)
fig = px.bar(df_ventas_dia, x="dia_nombre", y="total_ventas", title="Distribución de ventas por día de la semana")
st.plotly_chart(fig)

df_envios_anio = pd.read_sql("""
SELECT EXTRACT(YEAR FROM fecha_envio) AS anio, COUNT(*) AS total_envios
FROM logistica
GROUP BY anio
ORDER BY anio;
""", con=engine)

df_envios_anio['anio'] = df_envios_anio['anio'].astype(int)
df_envios_anio.rename(columns={"anio": "año"}, inplace=True)

st.subheader("Distribución de envíos por año")
st.write(df_envios_anio)

fig = px.bar(df_envios_anio, x=df_envios_anio["año"].astype(str), y="total_envios", 
             title="Distribución de envíos por año", labels={"año": "Año"})
fig.update_layout(xaxis_title="Año")

st.plotly_chart(fig)

df_envios_mes = pd.read_sql("""
SELECT TO_CHAR(fecha_envio, 'Month') AS mes_nombre, COUNT(*) AS total_envios
FROM logistica
GROUP BY mes_nombre
ORDER BY total_envios DESC;
""", con=engine)

st.subheader("Distribución de envíos por mes")
st.write(df_envios_mes)
fig = px.bar(df_envios_mes, x="mes_nombre", y="total_envios", title="Distribución de envíos por mes")
st.plotly_chart(fig)