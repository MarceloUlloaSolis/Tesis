# crear_red_apr_estructurada.py (ajustado a criterios técnicos APR Unión Río Blanco)
import wntr
import numpy as np
from wntr.network.io import write_inpfile

# Crear red
wn = wntr.network.WaterNetworkModel()

# Nodos principales
wn.add_junction('Sondaje', base_demand=0.0, elevation=90.0)
wn.add_tank('Estanque', elevation=115.0, init_level=10, min_level=5, max_level=15, diameter=12)
wn.add_junction('Nodo1', base_demand=0.0, elevation=105.0)

# Bomba desde sondaje al estanque
wn.add_curve('curva_bomba', 'HEAD', [(0, 25), (10, 25)])
wn.add_pump('B1', 'Sondaje', 'Estanque', 'HEAD', 'curva_bomba')

# Conexión desde Estanque a Nodo1
wn.add_pipe('P_E_N1', 'Estanque', 'Nodo1', length=30, diameter=0.15, roughness=100)

# Coordenadas para visualización
coords = {'Sondaje': (0, 300), 'Estanque': (0, 200), 'Nodo1': (0, 100)}

# Crear 5 ramas desde Nodo1 con 10 nodos cada una
total_nodos = 50
ramas = 5
nodos_por_rama = total_nodos // ramas
node_counter = 1
pipe_counter = 1

for r in range(ramas):
    base_x = (r - 2) * 100
    x, y = base_x, 100
    nodo_anterior = 'Nodo1'

    for i in range(nodos_por_rama):
        node_counter += 1
        pipe_counter += 1
        nodo_id = f'J{node_counter - 1}'
        pipe_id = f'P{pipe_counter - 1}'

        elev = round(np.random.uniform(95, 105), 3)
        wn.add_junction(nodo_id, base_demand=0.0, elevation=elev)  # demandas se asignan luego
        wn.add_pipe(pipe_id, nodo_anterior, nodo_id, length=60, diameter=0.075, roughness=100)

        y -= 30 + np.random.uniform(-5, 5)
        x += np.random.uniform(-10, 10)
        coords[nodo_id] = (x, y)
        nodo_anterior = nodo_id

# Asignar coordenadas
for node, (x, y) in coords.items():
    wn.get_node(node).coordinates = (x, y)

# Opciones de tiempo
wn.options.time.duration = 7 * 24 * 3600
wn.options.time.hydraulic_timestep = 15 * 60
wn.options.time.report_timestep = 15 * 60

# Guardar archivo
write_inpfile(wn, "epanet_sim/modelos/red_apr_estructurada.inp")
print("✅ Modelo ajustado con estanque a 125 m y nodos entre 95 y 105 m según criterios técnicos.")
