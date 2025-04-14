import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# Rutas a los archivos
ruta_presion = os.path.join("epanet_sim", "resultados", "presiones.csv")
ruta_caudal = os.path.join("epanet_sim", "resultados", "caudales.csv")

# Cargar datos con índice de tiempo real
df_presion = pd.read_csv(ruta_presion, index_col=0, parse_dates=True)
df_caudal = pd.read_csv(ruta_caudal, index_col=0, parse_dates=True)

# --- ELECCIÓN INTERACTIVA DEL NODO ---
print("\n📌 Nodos disponibles para presión:")
print(list(df_presion.columns))

while True:
    nodo_objetivo = input("🟦 Ingresa el ID del nodo a graficar (ej: 2): ")
    if nodo_objetivo in df_presion.columns:
        break
    print("❌ Nodo no válido. Intenta nuevamente.")

# --- ELECCIÓN INTERACTIVA DE LA TUBERÍA ---
print("\n📌 Enlaces disponibles para caudal:")
print(list(df_caudal.columns))

while True:
    tuberia_objetivo = input("🟩 Ingresa el ID de la tubería a graficar (ej: 1): ")
    if tuberia_objetivo in df_caudal.columns:
        break
    print("❌ Tubería no válida. Intenta nuevamente.")

# --- SELECCIÓN SIMPLIFICADA DEL RANGO DE TIEMPO ---
inicio_disponible = df_presion.index.min()
fin_disponible = df_presion.index.max()

print("\n📆 Datos disponibles desde:", inicio_disponible.strftime('%Y-%m-%d %H:%M'), "hasta", fin_disponible.strftime('%Y-%m-%d %H:%M'))

while True:
    try:
        dias = int(input("📅 ¿Cuántos días desde el inicio deseas graficar? (Ej: 1, 3, 7): "))
        break
    except ValueError:
        print("❌ Por favor, ingresa un número válido.")

fecha_inicio = inicio_disponible
fecha_fin = fecha_inicio + pd.Timedelta(days=dias)

# Filtrar datos
df_presion = df_presion.loc[fecha_inicio:fecha_fin]
df_caudal = df_caudal.loc[fecha_inicio:fecha_fin]

print(f"🟩 Mostrando datos desde {fecha_inicio} hasta {fecha_fin}")

# --- GRÁFICO DE PRESIÓN ---
plt.figure(figsize=(12, 5))
plt.plot(
    df_presion.index,
    df_presion[nodo_objetivo],
    label=f'Presión en nodo {nodo_objetivo}',
    color='darkblue',
    linewidth=2
)
plt.xlabel('Tiempo')
plt.ylabel('Presión (m)')
plt.title(f'Presión en el nodo {nodo_objetivo}')
plt.grid(True)
plt.legend()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)

# Autoescalado
valores = df_presion[nodo_objetivo]
min_val = valores.min()
max_val = valores.max()
if abs(max_val - min_val) < 0.01:
    plt.ylim(min_val - 0.5, max_val + 0.5)
else:
    margen = (max_val - min_val) * 0.1
    plt.ylim(min_val - margen, max_val + margen)

plt.tight_layout()
plt.savefig(os.path.join("epanet_sim", "graficos", f"presion_{nodo_objetivo}.png"))
plt.show()

# --- GRÁFICO DE CAUDAL ---
plt.figure(figsize=(12, 5))
plt.plot(
    df_caudal.index,
    df_caudal[tuberia_objetivo],
    label=f'Caudal en tubería {tuberia_objetivo}',
    color='darkgreen',
    linewidth=2
)
plt.xlabel('Tiempo')
plt.ylabel('Caudal (L/s)')
plt.title(f'Caudal en la tubería {tuberia_objetivo}')
plt.grid(True)
plt.legend()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b %H:%M'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)

# Autoescalado
valores = df_caudal[tuberia_objetivo]
min_val = valores.min()
max_val = valores.max()
if abs(max_val - min_val) < 0.01:
    plt.ylim(min_val - 0.5, max_val + 0.5)
else:
    margen = (max_val - min_val) * 0.1
    plt.ylim(min_val - margen, max_val + margen)

plt.tight_layout()
plt.savefig(os.path.join("epanet_sim", "graficos", f"caudal_{tuberia_objetivo}.png"))
plt.show()


