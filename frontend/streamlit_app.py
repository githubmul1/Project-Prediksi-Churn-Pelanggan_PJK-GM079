import streamlit as st
import pandas as pd
import os

from components.navbar import render_navbar
from components.footer import render_footer

# Konfigurasi Halaman 
st.set_page_config(
    page_title="Prediksi Churn Pelanggan",
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="collapsed" 
)

# Navbar 
menu_terpilih = render_navbar()

st.write("") 

# Main Content 
if menu_terpilih == "Dashboard":
    st.subheader("📈 Dashboard Analisis Churn")
    st.write("Berikut adalah visualisasi tren data pelanggan Anda saat ini.")
    
    # Menampilkan data dan grafik sederhana 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(current_dir, "..", "data", "raw", "ecommerce_customer_churn_data.csv"))
    
    try:
        df = pd.read_csv(csv_path)
        st.dataframe(df.head(10))
        
        kolom_numerik = df.select_dtypes(include=['number']).columns.tolist()
        if kolom_numerik:
            kolom_pilihan = st.selectbox("Pilih kolom untuk grafik:", kolom_numerik)
            st.line_chart(df[kolom_pilihan].head(100))
    except FileNotFoundError:
        st.error("File data tidak ditemukan.")

elif menu_terpilih == "Prediksi Churn":
    st.subheader("🔮 Form Prediksi Churn Pelanggan")
    st.write("Masukkan parameter di bawah ini untuk melihat probabilitas pelanggan akan churn.")
    
    # Contoh Form Input
    with st.form("form_prediksi"):
        umur = st.number_input("Umur Pelanggan", min_value=15, max_value=100, value=30)
        tenure = st.slider("Masa Berlangganan (Tenure - Bulan)", 0, 72, 12)
        monthly_charges = st.number_input("Biaya Bulanan ($)", min_value=0.0, value=50.0)
        
        submit_button = st.form_submit_button("Prediksi Sekarang")
        
        if submit_button:
            # Simulasi hasil prediksi
            st.info(f"Memproses data: Umur {umur}, Tenure {tenure} bulan, Biaya ${monthly_charges}")
            st.success("Hasil Prediksi: Pelanggan ini kemungkinan besar **TIDAK CHURN** (Kesetiaan Tinggi).")

elif menu_terpilih == "Tentang Aplikasi":
    st.subheader("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini dikembangkan oleh **Tim PJK-GM079** untuk memenuhi tugas proyek akhir.
    Menggunakan algoritma Machine Learning untuk memprediksi churn pelanggan berdasarkan pola perilaku historis.
    """)

render_footer()