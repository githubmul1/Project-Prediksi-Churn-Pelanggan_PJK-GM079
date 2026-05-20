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

    col = st.columns(1)
    with col[0]:
         st.markdown(
            '## <i class="fas fa-solid fa-clock-rotate-left"></i> 📖 Riwayat Prediksi',
            unsafe_allow_html=True,
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

    # Tabel Inferensi Lengkap Dengan Filter
    col_space, col_fil = st.columns([3, 1])
    with col_fil:
        available_risks = df["risk_level"].dropna().unique().tolist()
        filter_options = ["Semua"] + available_risks
        
        selected_risk = st.selectbox(
            label="Filter Berdasarkan Risiko:",
            options=filter_options,
            index=0,
            label_visibility="collapsed"
        )

    # Terapkan filter berdasarkan pilihan risiko
    df_clean_all = df.copy()
    df_clean_all.columns = df_clean_all.columns.str.replace('_', ' ').str.title()   
    if selected_risk != "Semua":
        df_filtered_base = df[df["risk_level"] == selected_risk]
    else:
        df_filtered_base = df.copy()

    # Siapkan data filter versi bersih untuk ditampilkan di tabel utama
    df_clean_filtered = df_filtered_base.copy()
    df_clean_filtered.columns = df_clean_filtered.columns.str.replace('_', ' ').str.title()

    # Membuat paginasi untuk tabel riwayat prediksi
    rows_per_page_history = 10
    total_rows_history = len(df_clean_filtered)
    total_pages = (total_rows_history - 1) // rows_per_page_history + (1 if total_rows_history % rows_per_page_history > 0 else 0)
    col_prev, col_info, col_next = st.columns([1, 2, 1])
                    
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    # Navigasi paginasi               
    with col_prev:
        if st.button("⬅️ Halaman Sebelumnya") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()

    with col_info:
        st.markdown(f"<div style='text-align: center; font-weight: bold; padding-top: 5px;'>Halaman {st.session_state.current_page} dari {total_pages}</div>", unsafe_allow_html=True)

    with col_next:
        if st.button("➡️ Halaman Berikutnya") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()

    start_idx = (st.session_state.current_page - 1) * rows_per_page_history
    end_idx = start_idx + rows_per_page_history
    df_paginated = df_clean_filtered.iloc[start_idx:end_idx]

    st.dataframe(df_paginated, use_container_width=True)

    st.caption(f"Menampilkan data pelanggan dari baris {start_idx + 1} hingga {min(end_idx, total_rows_history)} dari total {total_rows_history} hasil prediksi.")

    # Export CSV
    st.subheader("⬇️ Export Data")
    csv = df_clean_filtered.to_csv(index=False).encode("utf-8")
    file_name_csv = "churn_predictions_history.csv" if selected_risk == "Semua" else f"churn_history_{selected_risk.lower().replace(' ', '_')}.csv"
    
    st.download_button(
        label=f"Download CSV ({selected_risk})",
        data=csv,
        file_name=file_name_csv,
        mime="text/csv",
    )