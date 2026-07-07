import os
import streamlit as st
from dotenv import load_dotenv
from api_client import generador_modelos, generar

load_dotenv()
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render():
    st.subheader("Generador de versículos (modelos de n-gramas)")
    st.caption("La API construye modelos de n-gramas sobre el corpus y genera texto palabra por palabra.")

    try:
        modelos = generador_modelos(DEFAULT_API_URL)
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
            st.session_state["gen_resultado"] = generar(DEFAULT_API_URL, modeloSeleccionado, palabraInicial, largoMaximo)
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
