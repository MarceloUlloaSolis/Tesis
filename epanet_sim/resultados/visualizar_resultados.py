# visualizar_resultados.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# === CONFIGURACIÓN ===
archivo_presiones = "epanet_sim/resultados/presiones.csv"
archivo_caudales = "epanet_sim/resultados/caudales.csv"

# === CARGAR DATOS ===
presiones = pd.read_csv(archivo_presiones, index_col=0, parse_dates=True)
caudales = pd.read_csv(archivo_caudales, index_col=0, parse_dates=True)

# === OPCIONES ===
nodos_disponibles = presiones.columns.tolist()
tuberias_disponibles = caudales.columns.tolist()

print("\n📌 Nodos disponibles para presión:")
print(nodos_disponibles)
print("\n📌 Enlaces disponibles para caudal:")
print(tuberias_disponibles)

# === ELECCIÓN DEL USUARIO ===
nodo_seleccionado = input("\nIngresa el nombre del nodo a graficar presión (o presiona Enter para omitir): ")
tuberia_seleccionada = input("Ingresa el nombre del enlace a graficar caudal (o presiona Enter para omitir): ")

df = None
if nodo_seleccionado and nodo_seleccionado in presiones.columns:
    df = presiones[[nodo_seleccionado]]
    df.columns = [f"Presión en {nodo_seleccionado}"]
    df.plot(figsize=(12, 4), linewidth=1.2, color='royalblue')
    plt.ylabel("Presión (m.c.a.)")
    plt.title(f"Presión en el nodo {nodo_seleccionado} (1 bar ≈ 10 m)")
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}"))
    plt.tight_layout()
    plt.savefig(f"epanet_sim/graficos/presion_{nodo_seleccionado}.png")
    plt.show()

if tuberia_seleccionada and tuberia_seleccionada in caudales.columns:
    df = caudales[[tuberia_seleccionada]]
    df.columns = [f"Caudal en tubería {tuberia_seleccionada}"]
    df.plot(figsize=(12, 4), linewidth=1.2, color='seagreen')
    plt.ylabel("Caudal (L/s)")
    plt.title(f"Caudal en la tubería {tuberia_seleccionada}")
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.2f}"))
    plt.tight_layout()
    plt.savefig(f"epanet_sim/graficos/caudal_{tuberia_seleccionada}.png")
    plt.show()
