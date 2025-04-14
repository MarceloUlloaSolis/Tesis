# epanet_analysis.py
import wntr
import pandas as pd
import os

print("🔄 Cargando modelo...")

ruta_inp = "epanet_sim/modelos/red_apr_estructurada_patrones_limpio.inp"
wn = wntr.network.WaterNetworkModel(ruta_inp)

print("🚰 Ejecutando simulación hidráulica...")
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Validar que hay datos antes de continuar
if results.node is None or results.link is None:
    raise ValueError("❌ La simulación no generó resultados válidos.")

# Obtener presiones y caudales
presiones = results.node['pressure']
caudales = results.link['flowrate']

# Crear carpeta si no existe
output_dir = "epanet_sim/resultados"
os.makedirs(output_dir, exist_ok=True)

# Guardar como CSV (sobrescribe si ya existen)
presiones.to_csv(os.path.join(output_dir, "presiones.csv"))
caudales.to_csv(os.path.join(output_dir, "caudales.csv"))

print("✅ Simulación completada.")
print("📁 Archivos generados:")
print("   - epanet_sim/resultados/presiones.csv")
print("   - epanet_sim/resultados/caudales.csv")
