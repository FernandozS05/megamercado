import sys
import os
import pandas as pd
import re
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from etl.extract.extract_clientes import extraer_csv

def encontrar_id_faltante(ids_existentes):
    for i in range(1, max(ids_existentes) + 2): 
        if i not in ids_existentes:
            return i
    return max(ids_existentes) + 1

def limpiar_clientes(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = extraer_csv("clientes.csv")
    df.dropna(inplace=True)

    columnas_requeridas = ['cliente_id', 'nombre', 'edad', 'genero', 'ubicacion']
    if not set(columnas_requeridas).issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el archivo: {set(columnas_requeridas) - set(df.columns)}")

    df['nombre'] = df['nombre'].apply(lambda x: x.strip().title() if isinstance(x, str) else x)
    df['ubicacion'] = df['ubicacion'].apply(lambda x: x.strip().title() if isinstance(x, str) else x)
    df['genero'] = df['genero'].apply(lambda x: 'Masculino' if x == 'M' else ('Femenino' if x == 'F' else 'Otro'))

    def corregir_edad(edad):
        if isinstance(edad, (int, float)):
            if edad > 1000:
                return 100
            elif edad > 100:
                edad_str = str(int(edad)) 
                return int(edad_str[:2]) 
            elif isinstance(edad, float):
                edad_str = str(int(edad))
                return int(edad_str[:2])  
            elif 0 < edad <= 100:
                return int(edad)
        return edad

    df['edad'] = df['edad'].apply(corregir_edad)
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

    df['cliente_id'] = pd.to_numeric(df['cliente_id'], errors='coerce')
    ids_existentes = set(df['cliente_id'].dropna().astype(int))

    for index, row in df.iterrows():
        if np.isnan(row['cliente_id']):
            nuevo_id = encontrar_id_faltante(ids_existentes)
            df.at[index, 'cliente_id'] = nuevo_id
            ids_existentes.add(nuevo_id)
        elif row['cliente_id'] % 1 != 0:
            nuevo_id = encontrar_id_faltante(ids_existentes)
            df.at[index, 'cliente_id'] = nuevo_id
            ids_existentes.add(nuevo_id)
        else:
            df.at[index, 'cliente_id'] = int(row['cliente_id'])

    def ajustar_edad_fuera_rango(edad):
        if edad < 0 or edad > 100:
            edad_str = str(int(edad))
            return int(edad_str[:2])
        return edad

    df['edad'] = df['edad'].apply(ajustar_edad_fuera_rango)
    df = df[df['cliente_id'] > 0]
    df.drop_duplicates(subset=['cliente_id'], keep='first', inplace=True)

    df['cliente_id'] = df['cliente_id'].astype(int)

    df = df[columnas_requeridas]

    output_file = os.path.join(output_dir, "clientes_clean.csv")
    df.to_csv(output_file, index=False)
    
    print("Archivo Clientes limpiado correctamente.")

if __name__ == "__main__":
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(raiz_proyecto, "output")

    limpiar_clientes(output_path)