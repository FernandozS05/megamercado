import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

db_url = "postgresql://postgres:12345@localhost:5432/megamercado"
engine = create_engine(db_url)

st.title("Exploración de la base de datos")
st.markdown("<h3 style='color:#4CAF50;'>Tablas y su estructura.</h3>", unsafe_allow_html=True)

query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
"""
tablas = pd.read_sql(query, con=engine)

st.subheader("Tablas en la base de datos")
st.dataframe(tablas.style.set_table_styles([{
    'selector': 'thead th', 
    'props': [('background-color', '#4CAF50'), ('color', 'white')]
}, {
    'selector': 'tbody td',
    'props': [('color', 'black')]
}]), width=900)

for table in tablas["table_name"]:
    st.subheader(f"Estructura de la tabla: {table.capitalize()}")
    query = f"""
    SELECT column_name, data_type, 
           COALESCE(character_maximum_length::text, 'None') AS character_maximum_length
    FROM information_schema.columns
    WHERE table_name = '{table}'
    """
    estructura = pd.read_sql(query, con=engine)

    estructura['character_maximum_length'] = estructura['character_maximum_length'].apply(str)
    
    st.dataframe(estructura.style.set_table_styles([{
        'selector': 'thead th', 
        'props': [('background-color', '#4CAF50'), ('color', 'white')]
    }, {
        'selector': 'tbody td',
        'props': [('color', 'black')]
    }]), width=900)

st.subheader("Vista previa de los primeros 10 registros por tabla")
for table in tablas["table_name"]:
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 10", con=engine)

    columnas_float = ["precio_base", "precio_unitario", "total"]
    for col in columnas_float:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else '')

    if "sucursal_id" in df.columns:
        df["sucursal_id"] = pd.to_numeric(df["sucursal_id"], errors="coerce").fillna(0).astype(int)

    st.write(f"**{table.capitalize()}** - Primeros 10 registros:")
    st.dataframe(df.style.set_table_styles([{
        'selector': 'thead th', 
        'props': [('background-color', '#4CAF50'), ('color', 'white')]
    }, {
        'selector': 'tbody td',
        'props': [('color', 'black')]
    }]), width=900)

st.subheader("Valores nulos")
for table in tablas["table_name"]:
    df = pd.read_sql(f"SELECT * FROM {table}", con=engine)
    nulls = df.isnull().sum()
    
    if nulls.sum() > 0:
        st.write(f"**{table.capitalize()}** - Valores Nulos:")
        st.dataframe(nulls[nulls > 0].style.set_table_styles([{
            'selector': 'thead th', 
            'props': [('background-color', '#4CAF50'), ('color', 'white')]
        }, {
            'selector': 'tbody td',
            'props': [('color', 'black')]
        }]), width=900)
    else:
        st.write(f"**{table.capitalize()}** - Sin valores nulos")

st.subheader("Registros duplicados")
for table in tablas["table_name"]:
    df = pd.read_sql(f"SELECT * FROM {table}", con=engine)
    duplicates = df.duplicated().sum()
    st.write(f"**{table.capitalize()}** - Registros duplicados: {duplicates}")