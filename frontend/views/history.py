import os
import sys
import streamlit as st
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from database.connect_db import get_connection
from components.footer import render_footer

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_history():
    # Memuat CSS 
    css_path = os.path.abspath(os.path.join(current_dir, "../assets/css/style.css"))
    local_css(css_path)

    st.markdown("## ⏳ Riwayat Prediksi")
    st.markdown(
        """
        Di halaman ini, Anda dapat melihat riwayat prediksi churn pelanggan yang telah dilakukan sebelumnya. 
        Setiap entri dalam riwayat mencakup informasi tentang pelanggan, hasil prediksi, dan waktu prediksi dilakukan.
        """
    )

    # Ambil data dari database
    conn = get_connection()
    query = "SELECT * FROM predictions ORDER BY id DESC"
    df = pd.read_sql(query, conn)
    conn.close()

    if df is None or df.empty:
        st.info("💡 Belum ada data riwayat prediksi di dalam database.")
        return

    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.replace('_', ' ').str.title()

    # Tabel untuk pelanggan risiko tinggi
    st.subheader("🚨 Pelanggan Risiko Tinggi")
    
    high_risk_data = df[df["risk_level"].isin(["Critical Risk", "High Risk"])]
    
    if not high_risk_data.empty:
        high_risk_display = high_risk_data.copy()
        high_risk_display.columns = high_risk_display.columns.str.replace('_', ' ').str.title()
        st.dataframe(high_risk_display, use_container_width=True)
    else:
        st.info("💡 Tidak ada pelanggan dengan kategori risiko tinggi dalam riwayat saat ini.")

    # Tabel Inferensi Lengkap
    st.subheader("📋 Seluruh Riwayat Prediksi")
    st.dataframe(df_clean, use_container_width=True)

    # Export CSV
    st.subheader("⬇️ Export Data")
    csv = df_clean.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="churn_predictions_history.csv",
        mime="text/csv",
    )