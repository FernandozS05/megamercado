import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import json

db_url = "postgresql://postgres:12345@localhost:5432/megamercado"
engine = create_engine(db_url)

query = """
SELECT 
    v.producto_id,
    v.cantidad,
    v.precio_unitario,
    v.total,
    v.sucursal_id,
    p.categoria,
    p.precio_base,
    l.fecha_envio
FROM ventas v
JOIN logistica l ON v.venta_id = l.venta_id
JOIN productos p ON v.producto_id = p.producto_id;
"""

df = pd.read_sql(query, engine)

df["fecha_envio"] = pd.to_datetime(df["fecha_envio"])
df["sucursal_id"] = pd.to_numeric(df["sucursal_id"], errors='coerce').fillna(0).astype(int)
df["cantidad"] = df["cantidad"].astype(int)
df["precio_unitario"] = df["precio_unitario"].astype(float)
df["precio_base"] = df["precio_base"].astype(float)
df["total"] = df["total"].astype(float)

df['promedio_ventas_producto'] = df.groupby('producto_id')['cantidad'].transform('mean')
df['precio_promedio_sucursal'] = df.groupby('sucursal_id')['precio_unitario'].transform('mean')
df['estacion'] = df['fecha_envio'].dt.month % 12 // 3 + 1

df = pd.get_dummies(df, columns=["categoria"], drop_first=True)

X = df.drop(columns=["cantidad", "fecha_envio", "producto_id"])
y = df["cantidad"]

scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[['precio_unitario', 'precio_base', 'total']] = scaler.fit_transform(X[['precio_unitario', 'precio_base', 'total']])

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

mae_test = mean_absolute_error(y_test, y_pred)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred))
r2_test = r2_score(y_test, y_pred)

mae_train = mean_absolute_error(y_train, y_train_pred)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
r2_train = r2_score(y_train, y_train_pred)

print(f"🔹 MAE (Train): {mae_train} | MAE (Test): {mae_test}")
print(f"🔹 RMSE (Train): {rmse_train} | RMSE (Test): {rmse_test}")
print(f"🔹 R² (Train): {r2_train} | R² (Test): {r2_test}")

metricas = {
    "MAE_train": mae_train, "MAE_test": mae_test,
    "RMSE_train": rmse_train, "RMSE_test": rmse_test,
    "R²_train": r2_train, "R²_test": r2_test,
}
with open('metricas.json', 'w') as json_file:
    json.dump(metricas, json_file)

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5, color="blue", label="Predicciones")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='dashed', color='red', label="Línea Ideal")
plt.xlabel("Valores Reales")
plt.ylabel("Predicciones")
plt.legend()
plt.title("Predicciones vs Valores Reales")

plt.savefig('predicciones_vs_reales.png')

plt.show()