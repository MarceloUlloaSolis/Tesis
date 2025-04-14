# generar_fuga_sintetica.py
import pandas as pd
import numpy as np
import os

# === Configuración ===
archivo_presion_base = "epanet_sim/resultados/presiones.csv"
archivo_caudal_base = "epanet_sim/resultados/caudales.csv"
nodo_fuga = "J12"        # Nodo donde se simulará fuga (presión cae)
tuberia_fuga = "P12"     # Tubería donde se simulará fuga (caudal sube)
instante_fuga = "2025-01-04 12:00:00"  # Momento exacto en que inicia la fuga

# === Leer archivos base ===
presiones = pd.read_csv(archivo_presion_base, index_col=0, parse_dates=True)
caudales = pd.read_csv(archivo_caudal_base, index_col=0, parse_dates=True)

# === Crear copias para fuga ===
presiones_fuga = presiones.copy()
caudales_fuga = caudales.copy()

# === Lógica de modificación ===
# Bajar presión en nodo afectado desde el instante de fuga
presiones_fuga.loc[instante_fuga:, nodo_fuga] -= np.linspace(5, 20, len(presiones_fuga.loc[instante_fuga:]))

# Subir caudal en tramo afectado desde el instante de fuga
caudales_fuga.loc[instante_fuga:, tuberia_fuga] += np.linspace(0.5, 2.0, len(caudales_fuga.loc[instante_fuga:]))

# Simular efecto en vecinos cercanos al nodo y tramo afectado (en presión)
nodos_vecinos = [f"J{int(nodo_fuga[1:])+1}", f"J{int(nodo_fuga[1:])-1}"]
for vecino in nodos_vecinos:
    if vecino in presiones_fuga.columns:
        presiones_fuga.loc[instante_fuga:, vecino] -= np.linspace(2, 10, len(presiones_fuga.loc[instante_fuga:]))

# === Guardar resultados ===
os.makedirs("epanet_sim/resultados", exist_ok=True)
presiones_fuga.to_csv("epanet_sim/resultados/presiones_fuga.csv")
caudales_fuga.to_csv("epanet_sim/resultados/caudales_fuga.csv")

print("✅ Datos con fuga generados")
print(f"📉 Nodo afectado: {nodo_fuga} (presión reducida)")
print(f"💧 Tubería afectada: {tuberia_fuga} (caudal incrementado)")
