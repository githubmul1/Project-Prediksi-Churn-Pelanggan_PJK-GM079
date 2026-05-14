import streamlit as st
import pandas as pd
import os
import joblib
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
        path = os.path.join(DATA_DIR, "raw", "ecommerce_customer_churn_data.csv")
        data = pd.read_csv(path)

        train_df, test_df = train_test_split(
            data, test_size=0.2, random_state=42, stratify=data['Is_Churn']
            )
        
        model = joblib.load(MODEL_PATH)
        y_test = test_df['Is_Churn']
        X_test = test_df.drop("Is_Churn", axis=1)
        y_pred = model.predict(X_test)

        total_p = len(data)
        prediksi_c = test_df['Is_Churn'].sum() 
        
        # UI Widget
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Dataset", f"{total_p:,}", help="Gabungan Train & Test") # dataset diambil dari folder data/processed
        with col2:
            st.metric("Prediksi Churn", f"{prediksi_c}", delta="Data Test")
        with col3:
            st.metric("Akurasi Model", f"{acc:.1%}")
            
    except Exception as e:
        st.error(f"Gagal memuat data statistik: {e}")