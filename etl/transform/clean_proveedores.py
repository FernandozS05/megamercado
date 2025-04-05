import sys
import os
import pandas as pd
import re
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from etl.extract.extract_proveedores import extraer_csv

def encontrar_id_faltante(ids_existentes):
    for i in range(1, max(ids_existentes) + 2): 
        if i not in ids_existentes:
            return i
    return max(ids_existentes) + 1

def limpiar_proveedores(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = extraer_csv("proveedores.csv")
    df.dropna(inplace=True)

    columnas_requeridas = ['proveedor_id', 'nombre_proveedor', 'contacto', 'ubicacion']
    if not set(columnas_requeridas).issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el archivo: {set(columnas_requeridas) - set(df.columns)}")

    df['proveedor_id'] = pd.to_numeric(df['proveedor_id'], errors='coerce')

    ids_originales = df['proveedor_id'].copy()

    ids_existentes = set(df['proveedor_id'].dropna().astype(int))

    for index, row in df.iterrows():
        if np.isnan(row['proveedor_id']):
            nuevo_id = encontrar_id_faltante(ids_existentes)
            df.at[index, 'proveedor_id'] = nuevo_id
            ids_existentes.add(nuevo_id)
        elif row['proveedor_id'] % 1 != 0:
            nuevo_id = encontrar_id_faltante(ids_existentes)
            df.at[index, 'proveedor_id'] = nuevo_id
            ids_existentes.add(nuevo_id)
        else:
            df.at[index, 'proveedor_id'] = int(row['proveedor_id'])

    df = df[df['proveedor_id'] > 0]

    df = df.sort_values(by='proveedor_id').reset_index(drop=True)
    df['nombre_proveedor'] = df['nombre_proveedor'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['ubicacion'] = df['ubicacion'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df['nombre_proveedor'] = df['nombre_proveedor'].str.title()
    df['ubicacion'] = df['ubicacion'].str.title()

    def validar_correo(email):
        return email if isinstance(email, str) and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) else None

    df['contacto'] = df['contacto'].apply(validar_correo)

    df.drop_duplicates(subset=['proveedor_id'], keep='first', inplace=True)

    df['proveedor_id'] = df['proveedor_id'].astype(int)

    df = df[columnas_requeridas]

    output_file = os.path.join(output_dir, "proveedores_clean.csv")
    df.to_csv(output_file, index=False)
    
    print("Archivo Proveedores limpiado correctamente.")

if __name__ == "__main__":
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(raiz_proyecto, "output")

    limpiar_proveedores(output_path)