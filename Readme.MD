# 📚 Proyecto Diplomado en Gestión de Datos

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)
![Pandas 2.2.2](https://img.shields.io/badge/Pandas-2.2.2-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-ff4b4b)
![Plotly](https://img.shields.io/badge/Plotly-5.22.0-darkblue)
![Folium](https://img.shields.io/badge/Folium-0.16.0-green)

## 📌 Descripción del Proyecto

Este proyecto fue desarrollado como parte del **Diplomado en Gestión de Datos** de la Universidad Santo Tomás. Su propósito es fortalecer competencias en procesamiento, visualización y análisis de datos usando herramientas modernas como Python, SQL y Streamlit.

La aplicación principal permite:
- 📥 Cargar datos abiertos del Ministerio de Educación Nacional (MEN).
- 🔧 Transformar los datos en un modelo dimensional tipo estrella.
- 📊 Visualizar indicadores clave de cobertura educativa.
- 🗺️ Explorar estos indicadores en un mapa interactivo por departamento.

---

## 📁 Estructura del Proyecto

```text
📁 proyecto_diplomado/
│
├── app.py                         # App principal de Streamlit
├── cargar_datos.py               # Módulo para carga de datos desde la API del MEN
├── transformacion.py             # Limpieza, modelo estrella y métricas
├── visualizaciones.py            # Gráficos interactivos por año y región
├── mapa.py                       # Mapa coroplético con Folium
│
├── data_shapes/
│   └── MGN_ANM_DPTOS.shp         # Shapefile con límites departamentales
│
├── Retos/
│   └── reto_educacion.sql        # Reto de modelado SQL de cobertura neta
│
├── requirements.txt              # Dependencias del proyecto (para uso con Poetry o pip)
└── README.md                     # Este documento