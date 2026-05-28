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
    css_path = os.path.join(current_dir, "../assets/css/style.css")
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

    df_columns = df.columns.str.replace("_", " ").str.title()
    df.columns = df_columns

    # konversi datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Date"] = df["Timestamp"].dt.date

    # semua data terseleksi
    filtered_df = df.copy()

    # buat metrik
    total_predictions = len(filtered_df)  # total prediksi yang sudah dilakukan

    churn_rate = filtered_df["Prediction"].mean()  # tingkat churn

    avg_probability = filtered_df[
        "Churn Probability"
    ].mean()  # rata-rata probabilitas churn

    high_risk_count = len(
        filtered_df[filtered_df["Risk Level"].isin(["Critical Risk", "High Risk"])]
    )  # jumlah pelanggan risiko tinggi

    (
        col1,
        col2,
        col3,
        col4,
    ) = st.columns(
        4
    )  # bagi dalam 4 kolom

    with col1:  # kolom 1 total prediksi
        with st.container(border=True):
            st.metric("Total Prediksi", total_predictions)

    with col2:  # kolom 2 churn rate
        with st.container(border=True):
            st.metric("Churn Rate", f"{churn_rate:.1%}")

    with col3:  # kolom 3 rata-rata kemungkinan churn
        with st.container(border=True):
            st.metric("Rata-Rata Probabilitas Churn", f"{avg_probability:.1%}")

    with col4:  # kolom 4 jumlah pengguna dengan risiko churn tinggi
        with st.container(border=True):
            st.metric("Pelanggan Risiko Tinggi", high_risk_count)

    # buat 3 kolom berikutnya
    col_chart1, col_chart2, col_chart3 = st.columns(3)

    # tren harian
    with col_chart1:
        with st.container(border=True):
            st.subheader("📈 Tren Prediksi")

            trend_df = filtered_df.copy()

            trend_df["Date_Str"] = trend_df["Timestamp"].dt.strftime("%d-%m-%Y")

            trend_group = trend_df.groupby("Date_Str").size().reset_index(name="total")

            fig_trend = px.line(trend_group, x="Date_Str", y="total", markers=True)

            fig_trend.update_traces(line=dict(color="#0284C7", width=3))

            fig_trend.update_layout(
                xaxis_title="Tanggal",
                yaxis_title="Total Prediksi",
            )

            st.plotly_chart(fig_trend, use_container_width=True)

    # kolom 2 pie cart pengguna risiko tinggi
    with col_chart2:
        with st.container(border=True):
            st.subheader("⚠️ Level Risiko Pelanggan")

            risk_group = filtered_df["Risk Level"].value_counts().reset_index()

            risk_group.columns = ["Risk Level", "Count"]

            fig_risk = px.pie(risk_group, names="Risk Level", values="Count", hole=0.4)

            fig_risk.update_layout(paper_bgcolor="rgba(0,0,0,0)")

            color_map = {
                "Critical Risk": "#BF2C34",
                "High Risk": "#D35400",
                "Medium Risk": "#2980B9",
                "Low Risk": "#27AE60",
            }

            colors = [color_map.get(x, "#3B82F6") for x in risk_group["Risk Level"]]

            fig_risk.update_traces(marker=dict(colors=colors))

            st.plotly_chart(fig_risk, use_container_width=True)

    # kolom 3 jenis kontrak
    with col_chart3:
        with st.container(border=True):
            st.subheader("📑 Jenis Kontrak")

            contract_group = filtered_df["Contract Type"].value_counts().reset_index()

            contract_group.columns = ["Contract Type", "Count"]

            fig_contract = px.bar(contract_group, x="Contract Type", y="Count")

            fig_contract.update_traces(marker_color=["#343187", "#5C92F6"])

            fig_contract.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Jenis Kontrak",
                yaxis_title="Total Pelanggan",
            )

            st.plotly_chart(fig_contract, use_container_width=True)
