import sys
import os
import pandas as pd
import re
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from etl.extract.extract_ventas import extraer_csv

productos_df = pd.read_csv("C:/Users/ferna/Downloads/MegaMercado/etl/output/productos_clean.csv")
productos_dict = dict(zip(productos_df['producto_id'], productos_df['precio_base']))

clientes_df = pd.read_csv("C:/Users/ferna/Downloads/MegaMercado/etl/output/clientes_clean.csv")
clientes_set = set(clientes_df['cliente_id'])

def encontrar_id_faltante(ids_existentes):
    ids_existentes = [int(id) for id in ids_existentes if pd.notnull(id)]
    if not ids_existentes:
        return 1
    for i in range(1, max(ids_existentes) + 2): 
        if i not in ids_existentes:
            return i
    return max(ids_existentes) + 1

def validate_product_id(df, products_dict):
    def correct_product(row):
        product_id = row['producto_id']
        unit_price = row['precio_unitario']

        if product_id in products_dict:
            return int(product_id)

        unit_price_int = int(unit_price)
        possible = [p_id for p_id, p_price in products_dict.items() if int(p_price) == unit_price_int]

        return possible[0] if possible else None

    df['producto_id'] = df.apply(correct_product, axis=1)
    df.dropna(subset=['producto_id'], inplace=True)
    df['producto_id'] = df['producto_id'].astype(int)
    return df

def validate_customers_ids(df, existing_customers_ids):
    valid_customer_ids = []

    for index, row in df.iterrows():
        customer_id = row['cliente_id']

        customer_id = int(customer_id) if isinstance(customer_id, (int, float)) and customer_id == int(
            customer_id) else None

        if customer_id is not None and customer_id in existing_customers_ids:
            valid_customer_ids.append(int(customer_id))

    df = df[df['cliente_id'].isin(valid_customer_ids)].copy()
    df['cliente_id'] = df['cliente_id'].astype(int)
    return df

def limpiar_ventas(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = extraer_csv("ventas.csv")

    df.dropna(subset=['venta_id', 'fecha', 'producto_id', 'cliente_id'], inplace=True)

    columnas_requeridas = ['venta_id', 'fecha', 'producto_id', 'cantidad', 'precio_unitario', 'cliente_id', 'sucursal_id', 'total']
    if not set(columnas_requeridas).issubset(df.columns):
        raise ValueError(f"Faltan columnas necesarias en el archivo: {set(columnas_requeridas) - set(df.columns)}")
    
    df.columns = df.columns.str.strip()
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    def limpiar_ids(col):
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64', errors='ignore')

    limpiar_ids('venta_id')
    limpiar_ids('producto_id')
    limpiar_ids('cliente_id')
    limpiar_ids('sucursal_id')

    df = df[ (df['producto_id'] == df['producto_id'].astype(int)) &
             (df['cliente_id'] == df['cliente_id'].astype(int)) &
             (df['sucursal_id'] == df['sucursal_id'].astype(int)) ]

    df = df[df['producto_id'].apply(lambda x: pd.notnull(x) and x > 0)] 

    df = df[df['producto_id'] > 0]
    df = df[df['cliente_id'] > 0]

    df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce')
    df['precio_unitario'] = pd.to_numeric(df['precio_unitario'], errors='coerce')
    df['total'] = pd.to_numeric(df['total'], errors='coerce')

    df = df[(df['cantidad'] > 0) & (df['precio_unitario'] > 0) & (df['total'] > 0)]

    df['precio_unitario'] = df['precio_unitario'].round(2)
    df['total'] = df['total'].round(2)

    df['cantidad'] = df['cantidad'].astype(int)
    df['total'] = df['total'].astype(float)

    df = df[df['venta_id'] > 0]

    existing_ids = df['venta_id'].tolist()
    missing_id = encontrar_id_faltante(existing_ids)
    df['venta_id'] = df['venta_id'].apply(lambda x: missing_id if pd.isna(x) else x)

    df.drop_duplicates(subset=['venta_id'], keep='first', inplace=True)

    df = validate_product_id(df, productos_dict)
    df = validate_customers_ids(df, clientes_set)

    df = df[columnas_requeridas]
    output_file = os.path.join(output_dir, "ventas_clean.csv")
    df.to_csv(output_file, index=False)
    
    print("Archivo Ventas limpiado y validado correctamente.")

if __name__ == "__main__":
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(raiz_proyecto, "output")

    limpiar_ventas(output_path)