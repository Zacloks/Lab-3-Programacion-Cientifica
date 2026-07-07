import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from wordcloud import WordCloud
from api_client import versiculos_por_libro, longitud_promedio, top_palabras, nube_palabras

load_dotenv()
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render():
    st.sidebar.header("Filtros de Búsqueda")
    testamento_seleccionado = st.sidebar.selectbox("Testamento", ["Todos", "Old Testament", "New Testament"])
    libro_seleccionado = st.sidebar.text_input("Nombre del Libro (ej. Genesis, Matthew)", value="")
    capitulo_seleccionado = st.sidebar.text_input("Capítulo (dejar vacío para todo el libro)", value="")

    testamentos = {"Old Testament": "OT", "New Testament": "NT"}

    parametros = {}
    if testamento_seleccionado != "Todos":
        parametros["testamento"] = testamentos[testamento_seleccionado]
    if libro_seleccionado:
        parametros["libro"] = libro_seleccionado
    if capitulo_seleccionado.isdigit():
        parametros["capitulo"] = int(capitulo_seleccionado)

    try:
        columna1, columna2 = st.columns(2)

        with columna1:
            st.subheader("Cantidad de Versículos por Libro")
            datosVersiculos = versiculos_por_libro(DEFAULT_API_URL, parametros)

            if datosVersiculos:
                df = pd.DataFrame(list(datosVersiculos.items()), columns=["Nombre del Libro", "Total de Versículos"])
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.info("No se encontraron datos para los filtros aplicados.")

        with columna2:
            st.subheader("Longitud Promedio de Versículos")
            datosLongitud = longitud_promedio(DEFAULT_API_URL, parametros)

            if datosLongitud:
                df = pd.DataFrame(list(datosLongitud.items()), columns=["Nombre del Libro", "Longitud Promedio (Caracteres)"])
                st.dataframe(df, hide_index=True, use_container_width=True)
            else:
                st.info("No se encontraron datos para los filtros aplicados.")

        st.markdown("---")
        columna3, columna4 = st.columns(2)

        with columna3:
            st.subheader("Top Palabras más Frecuentes")
            datosTop = top_palabras(DEFAULT_API_URL, parametros)

            if datosTop:
                st.dataframe(datosTop, use_container_width=True)
            else:
                st.info("No se encontraron palabras")

        with columna4:
            st.subheader("Nube de Palabras")
            datosNube = nube_palabras(DEFAULT_API_URL, parametros)

            if datosNube:
                frecuenciasLimpias = {str(palabra): freq for palabra, freq in datosNube.items()}

                nube = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate_from_frequencies(frecuenciasLimpias)

                st.image(nube.to_image())
            else:
                st.info("No se encontraron palabras para generar la nube")

    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
        st.info("Asegúrate de que el servidor de FastAPI esté corriendo en la dirección configurada.")
