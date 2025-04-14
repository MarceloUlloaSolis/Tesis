import wntr
import matplotlib.pyplot as plt

# Cargar el modelo
wn = wntr.network.WaterNetworkModel("epanet_sim/modelos/red_apr_estructurada.inp")

# Crear gráfico
fig, ax = plt.subplots(figsize=(12, 10))
wntr.graphics.plot_network(
    wn,
    ax=ax,
    node_size=20,
    link_width=1.2,
    title="🔷 Red APR Estructurada (50 nodos)"
)

# Guardar imagen
plt.savefig("epanet_sim/graficos/red_apr_estructurada.png")
plt.show()
