import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from api_client import coordenadas

load_dotenv()
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def render():
    st.subheader("Visualizador de versículos (PCA / Word2Vec)")
    st.caption("Cada punto es un versículo proyectado a 2D/3D. Coloreado por testamento.")

    col1, col2 = st.columns(2)
    with col1:
        metodo_label = st.selectbox("Representación", ["PCA sobre TF-IDF", "Word2Vec"])
    with col2:
        dim = st.radio("Dimensiones", [2, 3], horizontal=True)

    metodo = "tfidf" if metodo_label == "PCA sobre TF-IDF" else "word2vec"

    try:
        puntos = coordenadas(DEFAULT_API_URL, metodo, dim)
    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
        return

    if not puntos:
        st.info("No hay datos para mostrar.")
        return

    df = pd.DataFrame(puntos)
    if dim == 2:
        fig = px.scatter(df, x="x", y="y", color="testamento", hover_data=["nombre_libro"])
    else:
        fig = px.scatter_3d(df, x="x", y="y", z="z", color="testamento", hover_data=["nombre_libro"])

    st.plotly_chart(fig, use_container_width=True)
