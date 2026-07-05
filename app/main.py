import os
import requests
import streamlit as st

from dotenv import load_dotenv

st.set_page_config(
    page_title = "Mi primera pagina",
    layout = "wide"
)

load_dotenv()

DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.title("Mi primer dashboard")