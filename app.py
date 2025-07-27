# 📁 app.py
import streamlit as st
from cargar_datos import show_data_tab
from transformacion import show_transform_tab
from visualizaciones import show_visualization_tab
from mapa import show_map_tab

st.set_page_config(
    page_title="Dashboard Educativo - MEN",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Dashboard Educativo de Colombia")

st.markdown("""
Esta aplicación interactiva permite analizar el comportamiento de indicadores claves del sistema educativo colombiano,
como la **tasa de matriculación**, la **cobertura neta** y la **cobertura bruta**, usando datos abiertos del Ministerio de Educación Nacional.

Explora los datos por año, departamento y municipio, e interpreta los resultados con apoyo de gráficos y mapas interactivos.
""")

tabs = st.tabs([
    "📥 Carga de Datos",
    "🔧 Transformación y Métricas",
    "📊 Visualizaciones",
    "🗺️ Mapa Interactivo"
])

with tabs[0]:
    show_data_tab()

with tabs[1]:
    show_transform_tab()

with tabs[2]:
    show_visualization_tab()

with tabs[3]:
    show_map_tab()