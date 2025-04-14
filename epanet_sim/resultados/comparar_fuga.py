# comparar_fuga.py
import pandas as pd
import matplotlib.pyplot as plt
import os

# === Configuración ===
nodo = "J12"
tubo = "P12"
folder = "epanet_sim/resultados"

# === Cargar datos ===
presion_normal = pd.read_csv(f"{folder}/presiones.csv", index_col=0, parse_dates=True)
presion_fuga = pd.read_csv(f"{folder}/presiones_fuga.csv", index_col=0, parse_dates=True)

caudal_normal = pd.read_csv(f"{folder}/caudales.csv", index_col=0, parse_dates=True)
caudal_fuga = pd.read_csv(f"{folder}/caudales_fuga.csv", index_col=0, parse_dates=True)

# === Comparar presiones ===
plt.figure(figsize=(12, 4))
plt.plot(presion_normal.index, presion_normal[nodo], label="Presión normal", color="steelblue")
plt.plot(presion_fuga.index, presion_fuga[nodo], label="Presión con fuga", color="crimson", linestyle="--")
plt.title(f"Comparación de presión en nodo {nodo}")
plt.xlabel("Tiempo")
plt.ylabel("Presión (m.c.a.)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f"{folder}/comparacion_presion_{nodo}.png")
plt.show()

# === Comparar caudales ===
plt.figure(figsize=(12, 4))
plt.plot(caudal_normal.index, caudal_normal[tubo], label="Caudal normal", color="seagreen")
plt.plot(caudal_fuga.index, caudal_fuga[tubo], label="Caudal con fuga", color="orange", linestyle="--")
plt.title(f"Comparación de caudal en tubería {tubo}")
plt.xlabel("Tiempo")
plt.ylabel("Caudal (L/s)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f"{folder}/comparacion_caudal_{tubo}.png")
plt.show()

print("✅ Gráficos comparativos generados")
