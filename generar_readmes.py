from pathlib import Path

# Diccionario con contenido de los README
readmes = {
    "epanet_sim/modelos/README.md": """# Modelos

Esta carpeta contiene los scripts y archivos base para la generación de modelos hidráulicos en EPANET.

## Contenido

- `crear_red_apr_estructurada.py`: genera una red tipo árbol con 50 nodos.
- `asignar_patrones_demanda.py`: agrega demandas diferenciadas y patrones horarios únicos por nodo.
- Archivos `.inp` y `.net`: modelos generados para simulación.
""",
    "epanet_sim/resultados/README.md": """# Resultados

Resultados de simulación hidráulica con EPANET y validación de demandas.

## Contenido

- `epanet_analysis.py`: corre la simulación hidráulica.
- `verificar_patrones.py`: muestra demanda y patrón horario por nodo.
- `presiones.csv`, `caudales.csv`: salidas numéricas por paso de tiempo.
""",
    "epanet_sim/graficos/README.md": """# Gráficos

Scripts y salidas gráficas de presiones y caudales.

## Contenido

- `graficar_resultados.py`: permite visualizar presión/caudal por nodo o tubería.
- Imágenes `.png` generadas automáticamente o manualmente.
""",
    "README.md": """# Proyecto de Tesis: Simulación de Sistemas de Agua Potable Rural

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
"""
}

# Crear todos los archivos README.md
for path, content in readmes.items():
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    with open(path_obj, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Todos los README.md fueron generados correctamente.")
