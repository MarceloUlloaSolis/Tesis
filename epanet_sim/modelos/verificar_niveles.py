import wntr
from pathlib import Path

# Cargar archivo de red
inp_path = Path("epanet_sim/modelos/red_apr_estructurada_patrones.inp")
wn = wntr.network.WaterNetworkModel(str(inp_path))

# Estanques
print("🏗️ Estanques:")
for nombre, tank in wn.tanks():
    print(f"  - Estanque: {nombre}")
    print(f"    • Elevación base      : {tank.elevation:.2f} m")
    print(f"    • Nivel inicial       : {tank.init_level:.2f} m")
    print(f"    • Nivel mínimo        : {tank.min_level:.2f} m")
    print(f"    • Nivel máximo        : {tank.max_level:.2f} m")
    print(f"    • Altura total actual : {tank.elevation + tank.init_level:.2f} m")

# Nodos (Junctions)
print("\n📍 Elevaciones de los primeros 10 nodos:")
for nombre, j in list(wn.junctions())[:10]:
    print(f"  - Nodo {nombre}: {j.elevation:.2f} m")

# Demandas
print("\n💧 Demandas base por nodo (L/s):")
for nombre, j in list(wn.junctions())[:10]:
    print(f"  - Nodo {nombre}: {j.demand_timeseries_list[0].base_value:.5f} L/s")


