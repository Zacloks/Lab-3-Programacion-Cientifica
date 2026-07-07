import os
import streamlit as st
from dotenv import load_dotenv
from api_client import generar

load_dotenv()
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render():
    st.subheader("Generador de versículos")
    st.caption("Elige un modelo de n-gramas y genera un versículo nuevo palabra por palabra.")

    modelo = st.selectbox("Modelo", ["unigram", "bigram", "trigram"])
    palabra_inicial = st.text_input("Palabra inicial (opcional)", value="")
    largo_maximo = st.slider("Largo máximo (palabras)", min_value=5, max_value=100, value=50)

    if st.button("Generar"):
        try:
            resultado = generar(DEFAULT_API_URL, modelo, palabra_inicial, largo_maximo)
            st.info(resultado["texto_generado"])
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
