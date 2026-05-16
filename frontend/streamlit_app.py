import streamlit as st
import pandas as pd
import os

import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from frontend import prediction
from frontend.components import about
from components.navbar import render_navbar
from components.footer import render_footer
from components.dashboard import render_stats_widgets

# Konfigurasi Halaman
st.set_page_config(
    page_title="Prediksi Churn Pelanggan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

menu = render_navbar()
if menu == "Dashboard":
    st.markdown(
        "### <img src='https://cdn-icons-png.flaticon.com/128/1041/1041888.png' width='40'> Dashboard Analisis",
        unsafe_allow_html=True,
    )
    st.info("Pilih menu **Prediksi Churn** di navigasi atas untuk memulai analisis.")
    render_stats_widgets()

elif menu == "Prediksi Churn":
    prediction.render_prediction()

elif menu == "Tentang Aplikasi":
    about.render_about()

render_footer()
