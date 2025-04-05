import sys
import os
import pandas as pd
import re
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )
from etl.extract.extract_ventas import extraer_csv

def limpiar_logistica(output_dir, ventas_clean_file, proveedores_clean_file):
    os.makedirs(output_dir, exist_ok=True)

    df = extraer_csv("logistica.csv")

    df.dropna(subset=['envio_id', 'venta_id', 'proveedor_id'], inplace=True)

    columnas_requeridas = ['envio_id', 'venta_id', 'fecha_envio', 'proveedor_id', 'estado_envio']
    if not set(columnas_requeridas).issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el archivo: {set(columnas_requeridas) - set(df.columns)}")
    
    df.columns = df.columns.str.strip()
    df['fecha_envio'] = pd.to_datetime(df['fecha_envio'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    def limpiar_ids(col):
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64', errors='ignore')

    limpiar_ids('envio_id')
    limpiar_ids('venta_id')
    limpiar_ids('proveedor_id')

    df = df[~df['envio_id'].apply(lambda x: isinstance(x, float) and x.is_integer() and x > 1e6)]
    df = df[~df['venta_id'].apply(lambda x: isinstance(x, float) and x.is_integer() and x > 1e6)]
    df = df[~df['proveedor_id'].apply(lambda x: isinstance(x, float) and x.is_integer() and x > 1e6)]

    df['envio_id'] = df['envio_id'].astype(int)
    df['venta_id'] = df['venta_id'].astype(int)
    df['proveedor_id'] = df['proveedor_id'].astype(int)

    ventas_clean_df = pd.read_csv(ventas_clean_file)
    valid_venta_ids = ventas_clean_df['venta_id'].unique()
    df = df[df['venta_id'].isin(valid_venta_ids)]

    proveedores_clean_df = pd.read_csv(proveedores_clean_file)
    valid_proveedor_ids = proveedores_clean_df['proveedor_id'].unique()
    df = df[df['proveedor_id'].isin(valid_proveedor_ids)]

    df.drop_duplicates(subset=['envio_id'], keep='first', inplace=True)

    df = df[~df.isnull().any(axis=1)]

    df = df.sort_values(by='envio_id')
    
    df['diferencia'] = df['envio_id'].diff().fillna(1)
    df = df[df['diferencia'] <= 2]
    df['diferencia_acumulada'] = df['envio_id'].diff().fillna(0)
    
    max_diferencia_permitida = 10000 
    df = df[df['diferencia_acumulada'] <= max_diferencia_permitida]

    df.drop(columns=['diferencia', 'diferencia_acumulada'], inplace=True)

    output_file = os.path.join(output_dir, "logistica_clean.csv")
    df.to_csv(output_file, index=False)
    
    print("Archivo Logística limpiado correctamente.")

if __name__ == "__main__":
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(raiz_proyecto, "output")
    ventas_clean_file = os.path.join(raiz_proyecto, "output", "ventas_clean.csv")
    proveedores_clean_file = os.path.join(raiz_proyecto, "output", "proveedores_clean.csv")

    limpiar_logistica(output_path, ventas_clean_file, proveedores_clean_file)