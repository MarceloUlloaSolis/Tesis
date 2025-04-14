import wntr
import numpy as np
from wntr.network.io import write_inpfile

# Cargar el modelo base
wn = wntr.network.WaterNetworkModel("epanet_sim/modelos/red_apr_estructurada.inp")

# Crear patrón base
patron_base = [
    0.05, 0.05, 0.05, 0.05, 0.05,
    0.25, 0.25,
    0.4, 0.4, 0.4,
    0.3, 0.3,
    0.7, 0.7,
    0.3, 0.3,
    0.7, 0.7, 0.7,
    0.15, 0.15, 0.15
]
while len(patron_base) < 24:
    patron_base.append(0.05)

# Parámetros de diseño
habitantes = 4
litros_dia = 125 * habitantes
consumo_base = litros_dia / 86400  # ≈ 0.0058 L/s

# Asignar demandas y patrones
for i in range(1, 51):
    nodo_id = f'J{i}'
    nodo = wn.get_node(nodo_id)

    # Variación individual de demanda
    variacion = np.random.uniform(0.85, 1.15)
    demanda = round(consumo_base * variacion, 6)

    # Crear patrón individual con ligeras variaciones horarias
    patron_ind = [round(v * np.random.uniform(0.9, 1.1), 3) for v in patron_base]
    patron_nombre = f'patron_{nodo_id}'
    wn.add_pattern(patron_nombre, patron_ind)

    # Eliminar cualquier demanda anterior
    nodo.demand_timeseries_list.clear()

    # ✅ Agregar demanda con patrón directamente
    nodo.add_demand(demanda, patron_nombre)

# Guardar archivo final
write_inpfile(wn, "epanet_sim/modelos/red_apr_estructurada_patrones.inp")
print("✅ Archivo .inp generado correctamente con patrones y demandas individuales.")

