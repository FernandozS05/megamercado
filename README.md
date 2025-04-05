# Proyecto MegaMercado

## Estructura del Proyecto

### 1. **Pipeline (etl/)**

- **`extract/`** → Scripts encargados de leer los datos desde los archivos CSV.
  - `extract_clientes.py`: Obtiene los datos del archivo `clientes.csv`.
  - `extract_logistica.py`: Obtiene los datos del archivo `logistica.csv`.
  - `extract_productos.py`: Obtiene los datos del archivo `productos.csv`.
  - `extract_proveedores.py`: Obtiene los datos del archivo `proveedores.csv`.
  - `extract_ventas.py`: Obtiene los datos del archivo `ventas.csv`.

- **`transform/`** → Scripts que realizan la limpieza y transformación de los datos extraídos.
  - `clean_clientes.py`: Elimina registros y ajusta los datos de clientes.
  - `clean_logistica.py`: Limpia y normaliza los datos de logística.
  - `clean_productos.py`: Ajusta y valida los datos de productos.
  - `clean_proveedores.py`: Realiza la limpieza de los datos de proveedores.
  - `clean_ventas.py`: Prepara los datos de ventas para el análisis.

- **`load/`** → Procesos de carga de los datos transformados en la base de datos.
  - `load.py`: Toma los datos procesados y los inserta en la base de datos.

- **`output/`** → Carpeta donde se almacenan los archivos CSV con los datos ya procesados y listos para cargar.
  - `clientes_clean.csv`: Datos de clientes después del proceso de limpieza.
  - `logistica_clean.csv`: Datos de logística depurados.
  - `productos_clean.csv`: Productos ya transformados.
  - `proveedores_clean.csv`: Proveedores limpios y validados.
  - `ventas_clean.csv`: Datos de ventas refinados.

- **`db/`** → Archivos relacionados con la base de datos.
  - `diagram.png`: Representación visual del modelo de base de datos.
  - `schema.sql`: Esquema SQL para la creación de la base de datos.

- **`__init__.py`**: Inicializa el paquete `etl` para su uso en otros módulos.

### 2. **Análisis Exploratorio de Datos (eda/)**

- `explorar_bd.py`: Realiza un análisis preliminar de la estructura y los datos en la base de datos.
- `explorar_datos.py`: Analiza los datos para identificar patrones y características clave.
- `explorar_fechas.py`: Estudia los aspectos temporales de los datos y su distribución.
- `explorar_tendencias.py`: Busca tendencias y patrones significativos dentro de los datos.

### 3. **Modelo Predictivo (model/)**

- `model.py`: Implementación del modelo de regresión lineal para la predicción de la demanda.
- `modelo_regresion_lineal.json`: Modelo entrenado listo para hacer predicciones.
- `metricas.json`: Archivo que contiene las métricas de rendimiento del modelo.
- `predicciones.csv`: Resultados de las predicciones generadas por el modelo.
- `predicciones_vs_reales.png`: Gráfico que compara las predicciones contra los valores reales.

### 4. **API (api/)**

- **`app/`** → Implementación de la API usando FastAPI.
  - `db.py`: Configuración y conexión de la base de datos para la API.
  - `models.py`: Definición de los modelos de datos que se usan en la API.
  - **`routes/`** → Archivos que definen las rutas de la API.
    - `router_clientes.py`: Rutas para interactuar con los datos de clientes.
    - `router_logistica.py`: Rutas para manejar los datos de logística.
    - `router_productos.py`: Rutas para la gestión de productos.
    - `router_proveedores.py`: Rutas para gestionar proveedores.
    - `router_ventas.py`: Rutas para consultar ventas.
  - **`main.py`**: Archivo principal que arranca la API.

### 5. **Dashboard (dashboard/)**

- `dash.py`: Archivo principal para la visualización interactiva de los datos mediante un dashboard.

### 6. **Data (data/)**

- `clientes.csv`: Información de clientes que se utiliza en el pipeline.
- `logistica.csv`: Información relacionada con los envíos de productos.
- `productos.csv`: Datos de los productos en inventario.
- `proveedores.csv`: Información sobre los proveedores.
- `ventas.csv`: Datos sobre las ventas realizadas.

## Instalación y Configuración  
Para ejecutar este proyecto, sigue estos pasos:  
- Clonar el repositorio y acceder a su directorio:  
  `git clone https://github.com/FernandozS05/megamercado.git`  
  `cd megamercado`  
- Instalar las dependencias:  
  `pip install -r requirements.txt`  

### 1. Accede al directorio cd etl/extract y ejecuta los siguientes scripts: 
Scripts para extraer datos desde archivos CSV:  
- `python extract_productos.py`  
- `python extract_clientes.py`  
- `python extract_proveedores.py`  
- `python extract_ventas.py`  
- `python extract_logistica.py`  

### 2. Accede al directorio cd etl/transform y ejecuta los siguientes scripts: 
Scripts de limpieza y transformación:  
- `python clean_productos.py`  
- `python clean_clientes.py`  
- `python clean_proveedores.py`  
- `python clean_ventas.py`  
- `python clean_logistica.py`  

### 3. Accede al directorio cd etl/db y realiza los siguientes pasos:
- Instalar PostgreSQL y una interfaz como DataGrip o PGAdmin  
- Crear base de datos llamada `megamercado`  
- Ejecutar script `schema.sql` en la consola  

### 4. Accede al directorio cd etl/load y ejecuta el siguiente script para cargar los datos transformados a la base de datos 
- `python load.py`  

### 5. Accede al directorio cd eda y ejecuta los siguientes comandos para abrir los notebooks de Streamlit que te permitirán visualizar los análisis en el navegador: 
- `streamlit run explorar_bd.py`  
- `streamlit run explorar_datos.py`  
- `streamlit run explorar_fechas.py`  
- `streamlit run explorar_tendencias.py`  

### 6. Accede al directorio cd model y ejecuta el siguiente comando para entrenar y generar las predicciones del modelo:
- `python model.py`  
 
### 7. Accede al directorio cd api y ejecuta el siguiente comando para iniciar el servidor de la API: 
- `uvicorn main:app --reload`  
  *Disponible en: http://127.0.0.1:8000/docs*
  
- La API debe estar en ejecución para acceder a la documentación.

### 8. Accede al directorio cd dashboard y ejecuta el siguiente comando para abrir el dashboard interactivo que consume la API: 
- `streamlit run dash.py`  