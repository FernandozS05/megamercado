import pandas as pd
from sqlalchemy import create_engine

db_url = "postgresql://postgres:12345@localhost:5432/megamercado"
engine = create_engine(db_url)

def load_csv_to_postgresql(csv_file_path, table_name, if_exists='append', id_columns=None):
    dtype = {col: 'Int64' for col in id_columns} if id_columns else {}
    df = pd.read_csv(csv_file_path, dtype=dtype)
    
    for col in id_columns:
        df[col] = df[col].fillna(0).astype('Int64')
    
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f"Datos cargados en la tabla '{table_name}' desde {csv_file_path}")

load_csv_to_postgresql("C:/Users/ferna/Downloads/MegaMercado/etl/output/productos_clean.csv", 
                       "productos", id_columns=['producto_id'])

load_csv_to_postgresql("C:/Users/ferna/Downloads/MegaMercado/etl/output/clientes_clean.csv", 
                       "clientes", id_columns=['cliente_id'])

load_csv_to_postgresql("C:/Users/ferna/Downloads/MegaMercado/etl/output/proveedores_clean.csv", 
                       "proveedores", id_columns=['proveedor_id'])

load_csv_to_postgresql("C:/Users/ferna/Downloads/MegaMercado/etl/output/ventas_clean.csv", 
                       "ventas", id_columns=['venta_id'])

load_csv_to_postgresql("C:/Users/ferna/Downloads/MegaMercado/etl/output/logistica_clean.csv", 
                       "logistica", id_columns=['envio_id'])