import os
import streamlit as st
from dotenv import load_dotenv
from api_client import api_get
import pandas as pd
from wordcloud import WordCloud

st.set_page_config(
    page_title = "Análisis del Corpus Bíblico",
    layout = "wide"
)

load_dotenv()
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("Análisis del Corpus Bíblico")

st.sidebar.title("Navegación")
seccion = st.sidebar.radio(
    "Sección",
    ["Dashboard", "Buscador", "Generador"],
    label_visibility = "collapsed",
)

if seccion == "Dashboard":
    st.sidebar.header("Filtros de Búsqueda")
    testamentoSeleccionado = st.sidebar.selectbox("Testamento", ["Todos", "Old Testament", "New Testament"])
    libroSeleccionado = st.sidebar.text_input("Nombre del Libro (ej. Genesis, Matthew)", value = "")
    capituloSeleccionado = st.sidebar.text_input("Capítulo (dejar vacío para todo el libro)", value = "")

    testamentos = {"Old Testament": "OT", "New Testament": "NT"}

    parametros = {}
    if testamentoSeleccionado != "Todos":
        parametros["testamento"] = testamentos[testamentoSeleccionado]
    if libroSeleccionado:
        parametros["libro"] = libroSeleccionado
    if capituloSeleccionado.isdigit():
        parametros["capitulo"] = int(capituloSeleccionado)

    try:
        columna1, columna2 = st.columns(2)

        with columna1:
            st.subheader("Cantidad de Versículos por Libro")
            datosVersiculos = api_get(DEFAULT_API_URL, "/dashboard/versiculos-por-libro", params = parametros)

            if datosVersiculos:
                df = pd.DataFrame(list(datosVersiculos.items()), columns=["Nombre del Libro", "Total de Versículos"])
                st.dataframe(df, hide_index = True, use_container_width = True)
            else:
                st.info("No se encontraron datos para los filtros aplicados.")

        with columna2:
            st.subheader("Longitud Promedio de Versículos")
            datosLongitud = api_get(DEFAULT_API_URL, "/dashboard/longitud-promedio", params = parametros)

            if datosLongitud:
                df = pd.DataFrame(list(datosLongitud.items()), columns=["Nombre del Libro", "Longitud Promedio (Caracteres)"])
                st.dataframe(df, hide_index = True, use_container_width = True)
            else:
                st.info("No se encontraron datos para los filtros aplicados.")

        st.markdown("---")
        columna3, columna4 = st.columns(2)

        with columna3:
            st.subheader("Top Palabras más Frecuentes")
            datosTop = api_get(DEFAULT_API_URL, "/dashboard/top-palabras", params = parametros)

            if datosTop:
                st.dataframe(datosTop, use_container_width = True)
            else:
                st.info("No se encontraron palabras")

        with columna4:
            st.subheader("Nube de Palabras")
            datosNube = api_get(DEFAULT_API_URL, "/dashboard/nube-palabras", params = parametros)

            if datosNube:
                frecuenciasLimpias = {str(palabra): freq for palabra, freq in datosNube.items()}

                nube = WordCloud(width=800, height=400, background_color="white",colormap="viridis").generate_from_frequencies(frecuenciasLimpias)

                st.image(nube.to_image())
            else:
                st.info("No se encontraron palabras para generar la nube")

    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
        st.info("Asegúrate de que el servidor de FastAPI esté corriendo en la dirección configurada.")

elif seccion == "Buscador":
    st.subheader("Buscador semántico")
    st.caption("Escribe una frase y la API devuelve los versículos más similares (TF-IDF + similitud coseno).")

    frase_ingresada = st.text_input("Frase a buscar:", value="")

    if frase_ingresada:
        try:
            frases_similares = api_get(DEFAULT_API_URL, "/buscador/buscar", params={"frase": frase_ingresada, "n": 20})
            if frases_similares:
                df_similares = pd.DataFrame(frases_similares)
                st.dataframe(df_similares, hide_index=True, use_container_width=True)
            else:
                st.info("No se encontraron versículos similares.")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")

elif seccion == "Generador":
    st.subheader("Generador de versículos (modelos de n-gramas)")
    st.caption("La API construye modelos de n-gramas sobre el corpus y genera texto palabra por palabra.")

    try:
        modelos = api_get(DEFAULT_API_URL, "/generador/modelos", params=None)
    except Exception:
        modelos = ["unigram", "bigram", "trigram"]

    col_modelo, col_palabra, col_largo = st.columns([1, 1, 1])
    with col_modelo:
        modeloSeleccionado = st.selectbox("Modelo", modelos, index=min(1, len(modelos) - 1))
    with col_palabra:
        palabraInicial = st.text_input("Palabra inicial (opcional)", value="")
    with col_largo:
        largoMaximo = st.slider("Largo máximo (palabras)", min_value=5, max_value=100, value=30)

    if st.button("Generar", type="primary"):
        try:
            st.session_state["gen_resultado"] = api_get(
                DEFAULT_API_URL,
                "/generador/generar",
                params={"modelo": modeloSeleccionado, "palabra_inicial": palabraInicial, "largo_maximo": largoMaximo},
            )
        except Exception as e:
            st.session_state["gen_resultado"] = None
            st.error(f"Error al generar texto: {e}")

    resultado = st.session_state.get("gen_resultado")
    if resultado:
        st.markdown("#### Versículo generado")
        st.markdown(f"> {resultado['texto_generado']}")

        termino_natural = resultado["cantidad_palabras"] < resultado["largo_maximo"]
        metrica1, metrica2, metrica3 = st.columns(3)
        metrica1.metric("Modelo", f"{resultado['modelo']} (n={resultado['n']})")
        metrica2.metric("Palabras generadas", resultado["cantidad_palabras"])
        metrica3.metric("Terminó", "naturalmente" if termino_natural else "por largo máximo")

        if resultado.get("palabra_inicial") and resultado.get("palabra_inicial_conocida") is False:
            st.warning(
                f"La palabra inicial '{resultado['palabra_inicial']}' no aparece en el corpus; "
                "el texto continúa usando la distribución unigrama."
            )
