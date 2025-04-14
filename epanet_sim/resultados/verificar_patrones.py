import wntr

# Cargar el modelo generado
wn = wntr.network.WaterNetworkModel("epanet_sim/modelos/red_apr_estructurada_patrones.inp")

# Verificar patrones en los primeros 5 nodos
for i in range(1, 6):
    nodo_id = f'J{i}'
    nodo = wn.get_node(nodo_id)
    ts = nodo.demand_timeseries_list[0]
    demanda = ts.base_value
    patron_obj = ts.pattern

    print(f"🟦 Nodo: {nodo_id}")
    print(f"   - Base demand: {demanda:.5f} L/s")

    if patron_obj:
        nombre = patron_obj.name
        valores = patron_obj.multipliers
        print(f"   - Patrón: {nombre}")
        print(f"   - Horas 0–5: {valores[:6]}")
    else:
        print("   - ⚠️ Sin patrón asignado")

    print("")



