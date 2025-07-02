import streamlit as st
import pandas as pd
import plotly.express as px
import requests

@st.cache_data
def cargar_divipola():
    url = "https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        # Normalizar nombres de columnas
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.normalize('NFKD')
            .str.encode('ascii', errors='ignore')
            .str.decode('utf-8')
            .str.replace(' ', '_')
        )

        # Renombrar columnas claves según lo disponible
        rename_dict = {
            'cod_dpto': 'codigo_departamento',
            'dpto': 'departamento_divipola',
            'cod_mpio': 'codigo_municipio',
            'nom_mpio': 'municipio_divipola',
            'latitud': 'latitud',
            'longitud': 'longitud'
        }
        df = df.rename(columns=rename_dict)

        # Validar columnas necesarias
        columnas_necesarias = {'codigo_municipio', 'latitud', 'longitud'}
        if not columnas_necesarias.issubset(df.columns):
            raise KeyError(f"❌ No se encontraron todas las columnas necesarias: {columnas_necesarias}")

        # Convertir y limpiar
        df['codigo_municipio'] = df['codigo_municipio'].str.zfill(5)
        df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
        df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
        df = df.dropna(subset=['codigo_municipio', 'latitud', 'longitud'])

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar datos de DIVIPOLA: {e}")
        return pd.DataFrame()


def show_map_tab():
    st.header("🗺️ Mapa de Cobertura Neta por Municipio")

    # Validar existencia de tablas
    if 'df_fact' not in st.session_state or 'dim_geo' not in st.session_state or 'dim_tiempo' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    # Cargar data
    df_fact = st.session_state['df_fact']
    dim_geo = st.session_state['dim_geo']
    dim_tiempo = st.session_state['dim_tiempo']

    # Unir tablas
    df = df_fact.merge(dim_geo, on='id_geo').merge(dim_tiempo, on='id_tiempo')

    # Validar que columnas necesarias existan
    if 'c_digo_departamento' not in df.columns or 'municipio' not in df.columns:
        st.error("❌ Las columnas 'c_digo_departamento' o 'municipio' no están presentes en los datos.")
        return

    # Crear código municipio de 5 dígitos
    df['codigo_municipio'] = df['c_digo_departamento'].astype(str).str.zfill(2) + df['municipio'].astype(str).str.zfill(3)

    # Cargar coordenadas
    df_coords = cargar_divipola()
    if df_coords.empty:
        st.stop()

    # Unir coordenadas
    df_map = df.merge(df_coords, on='codigo_municipio', how='left')

    # Filtro de año
    if 'a_o' not in df_map.columns:
        st.error("❌ La columna 'a_o' (año) no está disponible en los datos.")
        return

    anios = sorted(df_map['a_o'].dropna().unique(), reverse=True)
    if not anios:
        st.warning("⚠️ No hay años disponibles para visualizar.")
        return

    anio = st.selectbox("Selecciona el año a visualizar", anios)
    df_map = df_map[df_map['a_o'] == anio]

    # Verificación final
    df_map = df_map.dropna(subset=['latitud', 'longitud', 'cobertura_neta'])
    if df_map.empty:
        st.warning("⚠️ No hay datos con coordenadas válidas y cobertura neta para este año.")
        return

    # Visualización del mapa
    fig = px.scatter_mapbox(
        df_map,
        lat="latitud",
        lon="longitud",
        hover_name="municipio_divipola",
        hover_data={"departamento_divipola": True, "cobertura_neta": True},
        color="cobertura_neta",
        color_continuous_scale="YlOrRd",
        size="cobertura_neta",
        size_max=15,
        zoom=4,
        height=600
    )

    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)