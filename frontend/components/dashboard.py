import streamlit as st
import pandas as pd
import os

def render_stats_widgets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(current_dir, "..", "..")
    try:
        # Ambil data dari folder data/processed 
        train_df = pd.read_csv(os.path.join(root_dir, "data", "processed", "train_processed.csv"))
        test_df = pd.read_csv(os.path.join(root_dir, "data", "processed", "test_processed.csv"))
        
        total_p = len(train_df) + len(test_df)
        prediksi_c = test_df['Churn'].sum() if 'Churn' in test_df.columns else 0
        acc = 0.892 # akan disesaikan nanti
        
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