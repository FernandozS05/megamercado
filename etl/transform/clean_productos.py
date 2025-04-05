import sys
import os
import pandas as pd
import re
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from etl.extract.extract_productos import extraer_csv

def encontrar_id_faltante(ids_existentes):
    for i in range(1, max(ids_existentes) + 2): 
        if i not in ids_existentes:
            return i
    return max(ids_existentes) + 1

def limpiar_productos(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = extraer_csv("productos.csv")
    df.dropna(inplace=True)

    columnas_requeridas = ['producto_id', 'nombre_producto', 'categoria', 'precio_base']
    if not set(columnas_requeridas).issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el archivo: {set(columnas_requeridas) - set(df.columns)}")

    df['producto_id'] = pd.to_numeric(df['producto_id'], errors='coerce')

    ids_originales = df['producto_id'].copy()

    ids_existentes = set(df['producto_id'].dropna().astype(int))

    for index, row in df.iterrows():
        if np.isnan(row['producto_id']):
            nuevo_id = encontrar_id_faltante(ids_existentes)
            df.at[index, 'producto_id'] = nuevo_id
            ids_existentes.add(nuevo_id)
        elif row['producto_id'] % 1 != 0:
            nuevo_id = encontrar_id_faltante(ids_existentes)
            df.at[index, 'producto_id'] = nuevo_id
            ids_existentes.add(nuevo_id)
        else:
            df.at[index, 'producto_id'] = int(row['producto_id'])

    df = df[df['producto_id'] > 0]
    df['nombre_producto'] = df['nombre_producto'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['categoria'] = df['categoria'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['nombre_producto'] = df['nombre_producto'].str.title()
    df['categoria'] = df['categoria'].str.title()
    df['precio_base'] = pd.to_numeric(df['precio_base'], errors='coerce').fillna(0).round(2)
    df.drop_duplicates(subset=['producto_id'], keep='first', inplace=True)

    df['producto_id'] = df['producto_id'].astype(int)

    df = df[columnas_requeridas]

    output_file = os.path.join(output_dir, "productos_clean.csv")
    df.to_csv(output_file, index=False)
    
    print("Archivo Productos limpiado correctamente.")

if __name__ == "__main__":
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(raiz_proyecto, "output")

    limpiar_productos(output_path)