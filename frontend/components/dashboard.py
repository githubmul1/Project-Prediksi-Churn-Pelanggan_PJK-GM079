import streamlit as st
import pandas as pd
import os
import joblib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from config import DATA_DIR, MODEL_PATH


def render_stats_widgets():
    total_p = 0
    prediksi_c = 0
    acc = 0.0

    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(current_dir, "..", "..")
    try:
        # Ambil data dari folder data/processed
        path = os.path.join(DATA_DIR, "ecommerce_customer_churn_data.csv")
        data = pd.read_csv(path)

        train_df, test_df = train_test_split(
            data, test_size=0.2, random_state=42, stratify=data["Is_Churn"]
        )

        model = joblib.load(MODEL_PATH)
        y_test = test_df["Is_Churn"]
        X_test = test_df.drop("Is_Churn", axis=1)
        y_pred = model.predict(X_test)

        total_p = len(data)
        prediksi_c = test_df["Is_Churn"].sum()
        acc = accuracy_score(y_test, y_pred)

        # UI Widget
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Dataset", f"{total_p:,}", help="Data dari folder data")
        with col2:
            st.metric(
                "Potensi Churn",
                f"{prediksi_c}",
                delta=f"Ditemukan di {len(test_df)} Data Test",
            )
        with col3:
            st.metric(
                "Akurasi Model", f"{acc:.1%}", help="Performa Model Random Forest"
            )

        st.markdown("---")

        # Visualisasi dalam bentuk grafik / Bar Chart
        chart_col1 = st.columns(1)[0]

        with chart_col1:
            data["Satisfaction_Score"] = data["Satisfaction_Score"].astype(str)
            df_score = (
                data.groupby(["Satisfaction_Score", "Is_Churn"])
                .size()
                .reset_index(name="Jumlah")
            )

            fig_bar = px.bar(
                df_score,
                x="Satisfaction_Score",
                y="Jumlah",
                color="Is_Churn",
                barmode="group",
                category_orders={
                    "Satisfaction_Score": ["1", "2", "3", "4", "5"]
                },  # Mengunci urutan skor
                color_discrete_map={1: "#EF4444", 0: "#10B981"},
            )
            fig_bar.update_layout(
                xaxis_title="Skor Kepuasan", yaxis_title="Jumlah Pelanggan"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat data statistik: {e}")
