# simulador_telemetria_streamlit.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os

# === Cargar datos con fugas ===
presion_normal = pd.read_csv("epanet_sim/resultados/presiones.csv", index_col=0, parse_dates=True)
presion_fuga = pd.read_csv("epanet_sim/resultados/presiones_fuga.csv", index_col=0, parse_dates=True)
caudal_normal = pd.read_csv("epanet_sim/resultados/caudales.csv", index_col=0, parse_dates=True)
caudal_fuga = pd.read_csv("epanet_sim/resultados/caudales_fuga.csv", index_col=0, parse_dates=True)

# === Interfaz Streamlit ===
st.set_page_config(page_title="Simulador de Fugas de Agua", layout="wide")
st.title("🚰 Simulador de Fugas de Agua a través de Telemetría")

st.sidebar.header("⚙️ Parámetros de Simulación")
umbral_bajada_presion = st.sidebar.slider("Umbral de caída de presión (m)", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
umbral_subida_caudal = st.sidebar.slider("Umbral de aumento de caudal (L/s)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
retardo_simulacion = st.sidebar.slider("Velocidad de simulación (segundos entre pasos)", min_value=0.0, max_value=2.0, value=0.1, step=0.1)
iniciar = st.sidebar.button("▶️ Iniciar Simulación")
reiniciar = st.sidebar.button("🔄 Reiniciar Simulación")
pausar = st.sidebar.checkbox("⏸️ Pausar Simulación")

st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Nodos monitoreados:** {presion_fuga.shape[1]}")
st.sidebar.markdown(f"🧩 **Tuberías monitoreadas:** {caudal_fuga.shape[1]}")

if reiniciar:
    st.experimental_rerun()

if iniciar:
    status = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💡 Indicador de Presión")
        led_presion = st.empty()
    with col2:
        st.markdown("### 💧 Indicador de Caudal")
        led_caudal = st.empty()

    st.markdown("---")
    st.subheader("📈 Gráficos en Tiempo Real")
    col3, col4 = st.columns(2)
    graf_presion = col3.empty()
    graf_caudal = col4.empty()

    st.markdown("---")
    st.subheader("🟢 Visor de Estado por Nodo y Tubería")
    estado_nodos = st.empty()
    estado_tuberias = st.empty()

    alertas_presion = set()
    alertas_caudal = set()
    registro_alertas = []
    archivo_alertas = "epanet_sim/resultados/alertas.csv"

    nodos_seleccionados = ["J12", "J15"]
    tuberias_seleccionadas = ["P12", "P15"]
    mostrar_grafico_presion = {n: [] for n in nodos_seleccionados}
    mostrar_grafico_caudal = {p: [] for p in tuberias_seleccionadas}

    tiempos = presion_fuga.index
    estado_nodos_actual = {}
    estado_tuberias_actual = {}

    for t, ts in enumerate(tiempos):
        if pausar:
            time.sleep(0.1)
            continue

        presion_estado = "🟢 Normal"
        caudal_estado = "🟢 Normal"

        for nodo in presion_fuga.columns:
            p_val = presion_fuga.loc[ts, nodo]
            p_ref = presion_normal.loc[ts, nodo]
            dp = p_ref - p_val
            if nodo in nodos_seleccionados:
                mostrar_grafico_presion[nodo].append(p_val)
            if dp >= umbral_bajada_presion:
                if nodo not in alertas_presion:
                    presion_estado = "🔴 Fuga"
                    alertas_presion.add(nodo)
                    st.error(f"🚨 FUGA DETECTADA: Nodo {nodo} caída ≥ {dp:.2f} m")
                    registro_alertas.append({"tipo": "presion", "elemento": nodo, "delta": round(dp, 2), "timestamp": ts})
                estado_nodos_actual[nodo] = "🔴 Fuga"
            else:
                estado_nodos_actual[nodo] = "🟢"

        for tubo in caudal_fuga.columns:
            q_val = caudal_fuga.loc[ts, tubo]
            q_ref = caudal_normal.loc[ts, tubo]
            dq = q_val - q_ref
            if tubo in tuberias_seleccionadas:
                mostrar_grafico_caudal[tubo].append(q_val)
            if dq >= umbral_subida_caudal:
                if tubo not in alertas_caudal:
                    caudal_estado = "🔴 Fuga"
                    alertas_caudal.add(tubo)
                    st.warning(f"🚨 FUGA DETECTADA: Tubería {tubo} aumento ≥ {dq:.2f} L/s")
                    registro_alertas.append({"tipo": "caudal", "elemento": tubo, "delta": round(dq, 2), "timestamp": ts})
                estado_tuberias_actual[tubo] = "🔴 Fuga"
            else:
                estado_tuberias_actual[tubo] = "🟢"

        led_presion.markdown(f"**Presión:** {presion_estado}")
        led_caudal.markdown(f"**Caudal:** {caudal_estado}")

        figp, axp = plt.subplots()
        for nodo in nodos_seleccionados:
            axp.plot(mostrar_grafico_presion[nodo], label=f"Presión {nodo}")
        axp.legend()
        axp.set_ylabel("Presión (m.c.a.)")
        axp.set_xlabel("Tiempo")
        graf_presion.pyplot(figp)

        figc, axc = plt.subplots()
        for tubo in tuberias_seleccionadas:
            axc.plot(mostrar_grafico_caudal[tubo], label=f"Caudal {tubo}")
        axc.legend()
        axc.set_ylabel("Caudal (L/s)")
        axc.set_xlabel("Tiempo")
        graf_caudal.pyplot(figc)

        estado_nodos_df = pd.DataFrame(list(estado_nodos_actual.items()), columns=["Nodo", "Estado"])
        estado_tuberias_df = pd.DataFrame(list(estado_tuberias_actual.items()), columns=["Tubería", "Estado"])

        estado_nodos.dataframe(estado_nodos_df, hide_index=True, use_container_width=True)
        estado_tuberias.dataframe(estado_tuberias_df, hide_index=True, use_container_width=True)

        time.sleep(retardo_simulacion)

    if registro_alertas:
        df_alertas = pd.DataFrame(registro_alertas)
        df_alertas.to_csv(archivo_alertas, index=False)
        st.success(f"✅ Simulación finalizada. Alertas registradas en: {archivo_alertas}")
        st.markdown("### 📋 Resumen de Alertas Detectadas")
        st.dataframe(df_alertas)
        st.download_button(
            label="⬇️ Descargar Alertas CSV",
            data=df_alertas.to_csv(index=False).encode('utf-8'),
            file_name="alertas.csv",
            mime="text/csv"
        )

        st.markdown("### 📊 Gráfico resumen de elementos con fugas")
        resumen = df_alertas.groupby(["tipo", "elemento"]).size().reset_index(name="eventos")
        fig, ax = plt.subplots(figsize=(10, 4))
        resumen_plot = resumen.sort_values("eventos", ascending=False)
        ax.bar(resumen_plot["elemento"], resumen_plot["eventos"], color=["#007ACC" if t=="presion" else "#28A745" for t in resumen_plot["tipo"]])
        ax.set_xlabel("Elemento")
        ax.set_ylabel("Cantidad de eventos detectados")
        ax.set_title("Eventos detectados por nodo o tubería")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    else:
        st.success("✅ Simulación finalizada sin alertas detectadas.")


