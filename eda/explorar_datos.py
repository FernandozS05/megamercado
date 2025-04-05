import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

db_url = "postgresql://postgres:12345@localhost:5432/megamercado"
engine = create_engine(db_url)

st.title("Exploración de la distribución de los datos")

st.subheader("Distribución de categorías de los productos")
df_productos = pd.read_sql("SELECT categoria FROM productos", con=engine)
conteo_categorias = df_productos["categoria"].value_counts().reset_index()
conteo_categorias.columns = ["Categoría", "Cantidad"]
st.write(conteo_categorias)
fig = px.bar(conteo_categorias, x="Categoría", y="Cantidad", title="Distribución de categorías de los productos")
st.plotly_chart(fig)

st.subheader("Distribución del género de los clientes")
df_clientes = pd.read_sql("SELECT genero FROM clientes", con=engine)
conteo_genero = df_clientes["genero"].value_counts().reset_index()
conteo_genero.columns = ["Género", "Cantidad"]
st.write(conteo_genero)
fig = px.pie(conteo_genero, names="Género", values="Cantidad", title="Distribución del género de los clientes")
st.plotly_chart(fig)

st.subheader("Distribución de las ubicaciones de los clientes")
df_ubicacion = pd.read_sql("SELECT ubicacion FROM clientes", con=engine)
conteo_ubicacion = df_ubicacion["ubicacion"].value_counts().reset_index()
conteo_ubicacion.columns = ["Ubicación", "Cantidad"]
st.write(conteo_ubicacion)
fig = px.bar(conteo_ubicacion.head(10), x="Ubicación", y="Cantidad", title="Distribución de las ubicaciones de los clientes")
st.plotly_chart(fig)