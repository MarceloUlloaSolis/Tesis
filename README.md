# Proyecto de Tesis: Simulación de Sistemas de Agua Potable Rural

Este proyecto implementa la simulación de una red de agua potable rural utilizando **EPANET** y el paquete **WNTR** en Python. Se modela un sistema con 50 nodos de consumo, estanque elevado y bomba desde sondaje, considerando consumos realistas con patrones horarios diferenciados.

## 📁 Estructura del proyecto

- `epanet_sim/modelos/`: Scripts para generar modelos `.inp` y agregar demandas.
- `epanet_sim/resultados/`: Scripts de simulación y archivos resultantes (`.csv`, `.rpt`).
- `epanet_sim/graficos/`: Scripts de visualización y salidas gráficas.
- `data/`: Carpeta para archivos auxiliares o datos de entrada (vacía por ahora).
- `docs/`: Espacio reservado para documentación de la tesis.
- `tests/`: Carpeta opcional para pruebas automatizadas (si las incorporas).
- `requirements.txt`: Lista de dependencias necesarias.
- `README.md`: Este archivo.

## 🚀 Requisitos

Instalar dependencias desde consola con:

    pip install -r requirements.txt

## ⚙️ Tecnologías utilizadas

- Python 3.13+
- [WNTR](https://wntr.readthedocs.io/)
- [EPANET](https://www.epa.gov/water-research/epanet)
- Pandas, Matplotlib, NumPy

## 🧪 Flujo de trabajo sugerido

1. Crear modelo con `crear_red_apr_estructurada.py`
2. Asignar consumos y patrones con `asignar_patrones_demanda.py`
3. Verificar con `verificar_patrones.py`
4. Simular con `epanet_analysis.py`
5. Visualizar resultados con `graficar_resultados.py`

---

**Autor:** Marcelo Ulloa Solis  
**Entidad:** Subdirección de Servicios Sanitarios Rurales – MOP Región de La Araucanía  
