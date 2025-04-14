# graficar_todos.py
import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar datos
presiones = pd.read_csv("epanet_sim/resultados/presiones.csv", index_col=0, parse_dates=True)
caudales = pd.read_csv("epanet_sim/resultados/caudales.csv", index_col=0, parse_dates=True)

# Crear carpeta de gráficos si no existe
os.makedirs("epanet_sim/graficos", exist_ok=True)

# Graficar todas las presiones
for nodo in presiones.columns:
    plt.figure(figsize=(12, 4))
    plt.plot(presiones.index, presiones[nodo], label=f"Presión en {nodo}", color="steelblue")
    plt.xlabel("Tiempo")
    plt.ylabel("Presión (m.c.a.)")
    plt.title(f"Presión en el nodo {nodo}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"epanet_sim/graficos/presion_{nodo}.png")
    plt.close()

# Graficar todos los caudales
for tubo in caudales.columns:
    plt.figure(figsize=(12, 4))
    plt.plot(caudales.index, caudales[tubo], label=f"Caudal en {tubo}", color="seagreen")
    plt.xlabel("Tiempo")
    plt.ylabel("Caudal (L/s)")
    plt.title(f"Caudal en la tubería {tubo}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"epanet_sim/graficos/caudal_{tubo}.png")
    plt.close()

print("✅ Gráficos generados para todos los nodos y tuberías en 'epanet_sim/graficos/'")
