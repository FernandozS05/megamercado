import os
import pandas as pd

def extraer_csv(nombre_archivo, carpeta_data="data"):
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ruta_data = os.path.join(raiz_proyecto, carpeta_data)
    ruta_archivo = os.path.join(ruta_data, nombre_archivo)
    
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no se encontró.")
    
    return pd.read_csv(ruta_archivo, dtype=str, na_values=['', ' '])


if __name__ == "__main__":
    try:
        df_clientes = extraer_csv("clientes.csv")
        print("Archivo 'clientes.csv' cargado correctamente.")
    except FileNotFoundError as e:
        print(e)