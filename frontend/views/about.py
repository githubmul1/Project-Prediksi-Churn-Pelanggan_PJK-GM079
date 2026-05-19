import streamlit as st
from components.footer import render_footer

def render_about():
    st.markdown(
        '## <i class="fas fa-solid fa-circle-info"></i> Tentang Aplikasi',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        Aplikasi ini dirancang untuk membantu bisnis e-commerce dalam memprediksi risiko churn pelanggan.
        Dikembangkan menggunakan algoritma machine learning Random Forest, aplikasi diharapkan dapat memberikan wawasan tentang pelanggan yang berpotensi berhenti berlangganan, sehingga memungkinkan bisnis untuk mengambil tindakan proaktif dalam mempertahankan pelanggan.
        
        **Fitur Utama:**
        - **Dashboard Analisis:** Menampilkan statistik penting seperti total dataset, potensi churn, dan akurasi model.
        - **Prediksi Churn:** Form input untuk memasukkan data pelanggan dan mendapatkan prediksi risiko churn secara instan.
        
        **Teknologi yang Digunakan:**
        - Streamlit untuk antarmuka pengguna yang interaktif.
        - Scikit-learn untuk model machine learning.
        - Plotly untuk visualisasi data yang menarik.
        
        Aplikasi ini merupakan alat yang berguna bagi tim pemasaran dan manajemen untuk memahami perilaku pelanggan dan meningkatkan strategi retensi.
        """,
        unsafe_allow_html=True,
    )