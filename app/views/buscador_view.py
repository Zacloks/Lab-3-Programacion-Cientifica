import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from api_client import buscar

load_dotenv()
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render():
    st.subheader("Buscador semántico")
    st.caption("Escribe una frase y la API devuelve los versículos más similares (TF-IDF + similitud coseno).")

    frase_ingresada = st.text_input("Frase a buscar:", value="")

    if frase_ingresada:
        try:
            frases_similares = buscar(DEFAULT_API_URL, frase_ingresada, n=20)
            if frases_similares:
                df_similares = pd.DataFrame(frases_similares)
                st.dataframe(df_similares, hide_index=True, use_container_width=True)
            else:
                st.info("No se encontraron versículos similares.")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
