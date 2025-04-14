import wntr
import os
import pandas as pd


# Nombre del archivo .inp
nombre_modelo = "red_apr.inp"  # Cambia esto si tu archivo tiene otro nombre

# Ruta al modelo
modelo_path = os.path.join("epanet_sim", "modelos", nombre_modelo)

# Verificación del archivo
if not os.path.exists(modelo_path):
    print(f"❌ No se encontró el archivo: {modelo_path}")
    exit()

# Cargar la red hidráulica
print("🔄 Cargando el modelo EPANET...")
wn = wntr.network.WaterNetworkModel(modelo_path)
# ⏱ Simular 1 mes (30 días) con pasos de 15 minutos (900 segundos)
wn.options.time.duration = 30 * 24 * 3600          # 30 días en segundos
wn.options.time.hydraulic_timestep = 15 * 60       # 15 minutos = 900 segundos


# Ejecutar simulación hidráulica
print("🚰 Ejecutando simulación hidráulica...")
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Obtener dataframe de presiones y caudales
# Obtener resultados
pressure = results.node["pressure"]
flowrate = results.link["flowrate"]

# Obtener paso de tiempo y fechas
start_time = pd.Timestamp("2025-01-01 00:00:00")  # puedes cambiar la fecha base
time_step_min = wn.options.time.hydraulic_timestep / 60  # tiempo en minutos
n_steps = len(pressure)

# Crear índice de tiempo real
time_index = pd.date_range(start=start_time, periods=n_steps, freq=f"{int(time_step_min)}min")

# Aplicar índice a los DataFrames
pressure.index = time_index
flowrate.index = time_index


# Mostrar resumen
print("\n📊 Nodos disponibles:")
print(list(pressure.columns)[:5], "...")  # Muestra algunos nodos

print("\n📊 Primeras filas de presión:")
print(pressure.head())

print("\n🧵 Primeras filas de caudal:")
print(flowrate.head())

# Guardar como CSV (opcional)
pressure.to_csv("epanet_sim/resultados/presiones.csv")
flowrate.to_csv("epanet_sim/resultados/caudales.csv")

print("\n✅ Resultados guardados en carpeta 'resultados'")
