import streamlit as st
from frontend.components.footer import render_footer


def render_about():
    st.markdown(
        '## <i class="fas fa-solid fa-circle-info"></i> Tentang Aplikasi',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        Aplikasi ini dirancang dan dikembangkan oleh Tim PJK-GM079 untuk membantu bisnis e-commerce dalam memprediksi risiko churn pelanggan. Model machine learning yang digunakan dalam aplikasi ini dilatih menggunakan dataset pelanggan yang mencakup berbagai fitur seperti usia, jenis kelamin, lama berlangganan, dan interaksi dengan layanan, dimana ada **15.000** data pelanggan yang digunakan untuk melatih model. Dengan menggunakan algoritma Random Forest dan akurasi model mencapai **90.9%**, aplikasi ini dapat memberikan prediksi yang akurat tentang pelanggan yang berpotensi berhenti berlangganan, sehingga memungkinkan bisnis untuk mengambil tindakan proaktif dalam mempertahankan pelanggan.

        **Fitur Utama:**
        - **Dashboard Analisis:** Menampilkan statistik penting seperti total dataset, potensi churn, dan akurasi model.
        - **Prediksi Churn:** Form input dan upload file CSV untuk memasukkan data pelanggan dan mendapatkan prediksi risiko churn secara instan.
        - **Riwayat Prediksi:** Menyimpan dan menampilkan riwayat prediksi yang telah dilakukan, termasuk filter untuk melihat pelanggan dengan risiko tinggi.

        **Teknologi yang Digunakan:**
        - Streamlit untuk antarmuka pengguna yang interaktif.
        - Scikit-learn untuk model machine learning.
        - Plotly untuk visualisasi data yang menarik.

        Aplikasi ini merupakan alat yang berguna bagi tim pemasaran dan manajemen untuk memahami perilaku pelanggan dan meningkatkan strategi retensi.
        """,
        unsafe_allow_html=True,
    )
