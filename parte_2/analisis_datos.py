
# limpieza y estandarización de datos
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser

#leer el origen de los datos
df = pd.read_csv("ventas_2025.csv")

#print("Mostrando las primeras filas")
#print(df.head())

#print(df.describe())

# Mostrar faltantes
print("Identificar columnas faltantes")
print(df.isnull().sum())

#Tratamiento de valores
df['producto'] = df['producto'].fillna("Desconocido")
df['categoria'] = df['categoria'].fillna("Desconocido")
df['codigo_cliente'] = df['codigo_cliente'].fillna("Sin_codigo")
df['cantidad'] = df['cantidad'].fillna(0)

#eliminar simbolos en la columna precio_unitario (esto va ANTES que fillna y median)
df['precio_unitario'] = df['precio_unitario'].replace(r'[\$,]', '', regex=True).astype(float)

#AHORA sí puedes reemplazar los nulos con la mediana
df['precio_unitario'] = df['precio_unitario'].fillna(df['precio_unitario'].median())

#Tratamiento d valores nulos con la palanbra "Desconocido" y estandarizar a mayusculas
df['producto'] = df['producto'].str.upper()
df['categoria'] = df['categoria'].str.upper()
df['codigo_cliente'] = df['codigo_cliente'].str.upper()

# Conversión de fechas robusta
def parse_fecha(x):
    try:
        # Si está vacío o es NaN
        if pd.isnull(x) or str(x).strip() == "":
            return pd.NaT
        # Forzamos a str, quitamos espacios
        x = str(x).strip()
        # Usa dateutil, muy tolerante (mes en letras, etc.)
        dt = parser.parse(x, dayfirst=True, fuzzy=True)
        # Si el año es 2 dígitos, parser lo pone en el rango 1900-2099, fuerza a 2000s si hace falta
        if dt.year < 100:
            dt = dt.replace(year=dt.year + 2000)
        return dt
    except Exception as e:
        return pd.NaT

df['fecha'] = df['fecha'].apply(parse_fecha)

# Mostrar faltantes por segunda vez
print("Identificar columnas faltantes")
print(df.isnull().sum())

print("Mostrando las primeras filas")
print(df.head())




# Analisis y graficas
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# 1. los 3 productos más vendidos (por cantidad total)
top3_productos = df.groupby('producto')['cantidad'].sum().sort_values(ascending=False).head(3)
print("\nTop 3 productos más vendidos (por cantidad total):")
print(top3_productos)

# Gráfica de barras
top3_productos.plot(kind='bar', color='skyblue')
plt.title('Top 3 productos más vendidos (por cantidad)')
plt.xlabel('Producto')
plt.ylabel('Cantidad vendida')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2.ingresos totales por categoría
df['ingreso'] = df['cantidad'] * df['precio_unitario']
ingresos_categoria = df.groupby('categoria')['ingreso'].sum().sort_values(ascending=False)
print("\nIngresos totales por categoría:")
print(ingresos_categoria)

# Gráfica de barras
ingresos_categoria.plot(kind='bar', color='mediumseagreen')
plt.title('Ingresos totales por categoría')
plt.xlabel('Categoría')
plt.ylabel('Ingresos ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Mostrar los ingresos totales por mes en 2025
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
ingresos_mes = df[df['año'] == 2025].groupby('mes')['ingreso'].sum().sort_index()
print("\nIngresos totales por mes en 2025:")
print(ingresos_mes)

# Gráfica de líneas
ingresos_mes.plot(marker='o')
plt.title('Ingresos totales por mes en 2025')
plt.xlabel('Mes')
plt.ylabel('Ingresos ($)')
plt.xticks(ticks=range(1,13))
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# 4. Mostrar el código del cliente que más compró en cada mes del 2025 (por valor total de compras)
ventas_2025 = df[df['año'] == 2025]
clientes_mes = ventas_2025.groupby(['mes', 'codigo_cliente'])['ingreso'].sum().reset_index()
idx = clientes_mes.groupby('mes')['ingreso'].idxmax()
top_clientes_mes = clientes_mes.loc[idx].sort_values('mes')
print("\nCódigo del cliente que más compró en cada mes de 2025 (por valor total):")
print(top_clientes_mes[['mes', 'codigo_cliente', 'ingreso']])

# Gráfica de barras 
plt.figure(figsize=(10, 5))
plt.bar(top_clientes_mes['mes'].astype(str), top_clientes_mes['ingreso'], color='orange')
plt.title('Cliente con mayor compra por mes en 2025')
plt.xlabel('Mes')
plt.ylabel('Ingreso total ($)')
plt.xticks(rotation=0)

# Etiquetas de código de cliente
for i, row in enumerate(top_clientes_mes.itertuples()):
    plt.text(
        x=i,
        y=row.ingreso + max(top_clientes_mes['ingreso']) * 0.01,
        s=row.codigo_cliente,
        ha='center',
        va='bottom',
        fontsize=9,
        fontweight='bold'
    )

plt.tight_layout()
plt.show()
