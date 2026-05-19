import os
import streamlit as st
import pandas as pd
import plotly.express as px

from database.connect_db import get_connection

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/css/style.css")

def render_stats_widgets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "../../assets/css/style.css")
    local_css(css_path)

    conn = get_connection()

    query = """
    SELECT *
    FROM predictions
    ORDER BY id DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    # bila database masih kosong
    if df.empty:
        st.warning("Belum ada data prediksi.")
        return

    # konversi datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["date"] = df["timestamp"].dt.date

    # semua data terseleksi
    filtered_df = df.copy()

    # buat metrik
    total_predictions = len(filtered_df)  # total prediksi yang sudah dilakukan

    churn_rate = filtered_df["prediction"].mean()  # tingkat churn

    avg_probability = filtered_df[
        "churn_probability"
    ].mean()  # rata-rata probabilitas churn

    high_risk_count = len(
        filtered_df[filtered_df["risk_level"].isin(["Critical Risk", "High Risk"])]
    )  # jumlah pelanggan risiko tinggi

    col1, col2, col3, col4 = st.columns(4)  # bagi dalam 4 kolom

    with col1:  # kolom 1 total prediksi
        with st.container(border=True):
            st.metric("Total Prediksi", total_predictions)

    with col2:  # kolom 2 churn rate
        with st.container(border=True):
            st.metric("Churn Rate", f"{churn_rate:.1%}")

    with col3:  # kolom 3 rata-rata kemungkinan churn
        with st.container(border=True):
            st.metric("Avg Churn Probability", f"{avg_probability:.1%}")

    with col4:  # kolom 4 jumlah pengguna dengan risiko churn tinggi
        with st.container(border=True):
            st.metric("High Risk Customer", high_risk_count)

    st.markdown("---")  # buat garis

    # buat 3 kolom berikutnya
    col1, col2, col3 = st.columns(3)

    # tren harian
    with col1:

        st.subheader("📈 Tren Prediksi")

        trend_df = filtered_df.copy()

        trend_df["date"] = trend_df["timestamp"].dt.strftime("%d-%m-%Y")

        trend_group = trend_df.groupby("date").size().reset_index(name="total")

        fig_trend = px.line(trend_group, x="date", y="total", markers=True)

        st.plotly_chart(fig_trend, use_container_width=True)

    # kolom 2 pie cart pengguna risiko tinggi
    with col2:

        st.subheader("⚠️ Risk Level")

        risk_group = filtered_df["risk_level"].value_counts().reset_index()

        risk_group.columns = ["risk level", "count"]

        fig_risk = px.pie(risk_group, names="risk level", values="count", hole=0.4)

        st.plotly_chart(fig_risk, use_container_width=True)

    # kolom 3 jenis kontrak
    with col3:

        st.subheader("📑 Jenis Kontrak")

        contract_group = filtered_df["contract_type"].value_counts().reset_index()

        contract_group.columns = ["contract type", "count"]

        fig_contract = px.bar(contract_group, x="contract type", y="count")

        st.plotly_chart(fig_contract, use_container_width=True)
