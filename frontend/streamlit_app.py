import streamlit as st
import pandas as pd
import os

import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from frontend.views import prediction
from frontend.views import about
from frontend.components.navbar import render_navbar
from frontend.components.footer import render_footer
from frontend.views.dashboard import render_stats_widgets
from database.init_db import init_db

init_db()

# Konfigurasi Halaman
st.set_page_config(
    page_title="Prediksi Churn Pelanggan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

menu = render_navbar()
if menu == "Dashboard":

    render_stats_widgets()

elif menu == "Prediksi Churn":
    prediction.render_prediction()

elif menu == "Tentang Aplikasi":
    about.render_about()

render_footer()
