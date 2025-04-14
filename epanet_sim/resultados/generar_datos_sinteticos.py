# generar_datos_sinteticos.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

# Configuración general
n_nodos = 50
n_tuberias = 50
paso_minutos = 15
dias = 7
n_pasos = int((24*60/paso_minutos) * dias)

inicio = datetime(2025, 1, 1, 0, 0)
tiempo = [inicio + timedelta(minutes=i*paso_minutos) for i in range(n_pasos)]

# Generar datos de presión: nodos J1 a J50
presiones = pd.DataFrame(index=tiempo)
for i in range(1, n_nodos+1):
    base = np.random.uniform(35, 50)
    variacion = np.sin(np.linspace(0, 6*np.pi, n_pasos)) * np.random.uniform(1, 4)
    presiones[f"J{i}"] = base + variacion + np.random.normal(0, 0.5, n_pasos)

# Generar datos de caudal: tramos P1 a P50
caudales = pd.DataFrame(index=tiempo)
for i in range(1, n_tuberias+1):
    pico_am = np.sin(np.linspace(0, 2*np.pi, n_pasos)) * np.random.uniform(0.3, 0.7)
    pico_pm = np.sin(np.linspace(0, 2*np.pi, n_pasos) + np.pi) * np.random.uniform(0.2, 0.5)
    ruido = np.random.normal(0, 0.1, n_pasos)
    caudales[f"P{i}"] = 1.0 + pico_am + pico_pm + ruido

# Crear carpeta si no existe
os.makedirs("epanet_sim/resultados", exist_ok=True)

# Exportar CSV
presiones.to_csv("epanet_sim/resultados/presiones.csv")
caudales.to_csv("epanet_sim/resultados/caudales.csv")

print("✅ Datos sintéticos generados con 50 nodos y 50 tuberías por 7 días.")
