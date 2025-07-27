import streamlit as st
import pandas as pd
import requests

# ===============================================
# Cargar datos desde API
# ===============================================
def load_data_from_api(limit: int = 50000) -> pd.DataFrame:
    api_url = f"https://www.datos.gov.co/resource/nudc-7mev.json?$limit={limit}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")
    return pd.DataFrame()

# ===============================================
# Pestaña de carga de datos
# ===============================================
def show_data_tab():
    st.header("📥 Carga de Datos del MEN vía API")

    st.markdown("""
    Este conjunto de datos proviene del portal [datos.gov.co](https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/nudc-7mev).

    Presiona el botón para cargar los datos directamente desde la API.
    """)

    if st.button("🔄 Cargar datos"):
        with st.spinner("Cargando datos desde la API..."):
            df_raw = load_data_from_api()

        if df_raw is not None and not df_raw.empty:
            st.session_state['df_raw'] = df_raw
            st.success(f"¡Datos cargados exitosamente! ({len(df_raw)} filas)")
            st.dataframe(df_raw.head(10))

            st.markdown("**Resumen rápido de los datos:**")
            st.write("Años disponibles:", sorted(df_raw['a_o'].unique()))
            st.write("Departamentos:", df_raw['departamento'].nunique())
        else:
            st.warning("No se encontraron datos o hubo un error en la carga.")
    else:
        st.info("Presiona el botón para iniciar la carga.")