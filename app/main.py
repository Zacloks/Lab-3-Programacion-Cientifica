import os
import streamlit as st
from views import dashboard_view, buscador_view, generador_view
from dotenv import load_dotenv

DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title = "Análisis del Corpus Bíblico",
    layout = "wide"
)

load_dotenv()

with st.sidebar:
    vista = st.selectbox(
        "Selector de vista",
        (
            "Dasboard", "Buscador", "Visualizador", "Generador"
        )
    )

if vista == "Dasboard":
    dashboard_view.render()
elif vista == "Buscador":
    buscador_view.render()
elif vista == "Visualizador":
    pass    
else:
    generador_view.render()