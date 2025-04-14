import wntr
import numpy as np
from wntr.network.io import write_inpfile

# Cargar modelo base
inp_path = 'epanet_sim/modelos/red_apr_estructurada.inp'
wn = wntr.network.WaterNetworkModel(inp_path)

# Crear patrón de 96 pasos (cada 15 minutos)
patron_base = []
for t in range(96):
    hora = t * 15 / 60
    if 6 <= hora < 9:
        patron_base.append(1.5)
    elif 12 <= hora < 14:
        patron_base.append(1.2)
    elif 20 <= hora < 23:
        patron_base.append(1.4)
    elif 0 <= hora < 5:
        patron_base.append(0.3)
    else:
        patron_base.append(0.8)

# Agregar el patrón al modelo
nombre_patron = 'PATRON_HORARIO'
wn.add_pattern(nombre_patron, patron_base)

# Parámetros de consumo
lts_dia = 125
habitantes = 4
lts_totales = lts_dia * habitantes  # 500 L/día

# Asignar base_value y pattern al objeto existente
for nombre, j in wn.junctions():
    if 'J' in nombre:
        variacion = np.random.uniform(0.8, 1.2)
        base = float(round((lts_totales / 86400) * variacion, 5))  # L/s
        j.demand_timeseries_list[0].base_value = base
        j.demand_timeseries_list[0].pattern_name = nombre_patron  # ✅ nombre como string

# Guardar archivo generado
write_inpfile(wn, 'epanet_sim/modelos/red_apr_estructurada_patrones.inp')
print("✅ ¡Modelo con demandas y patrón horario creado con éxito!")

