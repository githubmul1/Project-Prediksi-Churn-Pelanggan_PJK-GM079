import streamlit as st
import pandas as pd
import os

st.title("Prediksi Churn Pelanggan")
st.write("Masukkan data pelanggan untuk memprediksi apakah mereka akan churn atau tidak.")

# Mendapatkan path ke file CSV secara dinamis
current_dir = os.path.dirname(__file__)
csv_path = os.path.abspath(os.path.join(current_dir, "..", "data", "raw", "ecommerce_customer_churn_data.csv"))

try:
    df = pd.read_csv(csv_path)
    st.success("Data berhasil dimuat!")
    
    # menampilkan 10 baris pertama 
    st.subheader("Preview Data Pelanggan")
    st.dataframe(df.head(10))
    
    # Membuat grafik dari kolom numerik yang valid
    st.subheader("Grafik Tren Data")
    
    # Deteksi kolom numerik otomatis agar aman dari error tipe data campuran
    kolom_numerik = df.select_dtypes(include=['number']).columns.tolist()
    
    if kolom_numerik:
        # user memilih kolom mana yang ingin dijadikan grafik
        kolom_pilihan = st.selectbox("Pilih kolom untuk ditampilkan di grafik:", kolom_numerik)
        st.line_chart(df[kolom_pilihan].head(100)) # Menampilkan 100 data pertama
    else:
        st.warning("Tidak ditemukan kolom numerik untuk membuat grafik.")

except FileNotFoundError:
    st.error(f"File CSV tidak ditemukan di lokasi: {csv_path}")