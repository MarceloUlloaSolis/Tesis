import wntr
import numpy as np
from wntr.network.io import write_inpfile

wn = wntr.network.WaterNetworkModel()

# Nodos principales
wn.add_junction('Sondaje', base_demand=0.0, elevation=90)
wn.add_tank('Estanque', elevation=100, init_level=5, min_level=1, max_level=10, diameter=12)
wn.add_junction('Nodo1', base_demand=0.0, elevation=99)

# Bomba desde sondaje al estanque
wn.add_curve('curva_bomba', 'HEAD', [(0, 25), (10, 25)])
wn.add_pump('B1', 'Sondaje', 'Estanque', 'HEAD', 'curva_bomba')

# Conexión Estanque → Nodo1
wn.add_pipe('P_E_N1', 'Estanque', 'Nodo1', length=30, diameter=0.15, roughness=100)

# Coordenadas
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

        elev = 95 + np.random.uniform(-1, 1)
        demanda = 0.5 + np.random.uniform(-0.2, 0.2)
        wn.add_junction(nodo_id, base_demand=demanda, elevation=elev)
        wn.add_pipe(pipe_id, nodo_anterior, nodo_id, length=60, diameter=0.075, roughness=100)

        y -= 30 + np.random.uniform(-5, 5)
        x += np.random.uniform(-10, 10)
        coords[nodo_id] = (x, y)
        nodo_anterior = nodo_id

# Asignar coordenadas
for node, (x, y) in coords.items():
    wn.get_node(node).coordinates = (x, y)

# Configuración de simulación
wn.options.time.duration = 7 * 24 * 3600
wn.options.time.hydraulic_timestep = 15 * 60
wn.options.time.report_timestep = 15 * 60

# Guardar el archivo
write_inpfile(wn, "epanet_sim/modelos/red_apr_estructurada.inp")
print("✅ Archivo generado: red_apr_estructurada.inp")
    