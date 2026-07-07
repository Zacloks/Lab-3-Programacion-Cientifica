import streamlit as st
from views import dashboard_view, buscador_view, generador_view, visualizador_view

st.set_page_config(
    page_title = "Análisis del Corpus Bíblico",
    layout = "wide"
)

with st.sidebar:
    vista = st.selectbox(
        "Selector de vista",
        (
            "Dashboard", "Buscador", "Visualizador", "Generador"
        )
    )

if vista == "Dashboard":
    dashboard_view.render()
elif vista == "Buscador":
    buscador_view.render()
elif vista == "Visualizador":
    visualizador_view.render()
else:
    generador_view.render()