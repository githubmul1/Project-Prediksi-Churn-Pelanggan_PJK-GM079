import streamlit as st
import pandas as pd
import joblib
import os

import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.inference import predict_churn
from components.navbar import render_navbar
from components.footer import render_footer
from components.dashboard import render_stats_widgets

# Konfigurasi Halaman
st.set_page_config(
    page_title="Prediksi Churn Pelanggan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

menu = render_navbar()
st.info("Pilih menu **Prediksi Churn** di navigasi atas untuk memulai analisis.")
if menu == "Dashboard":
    st.markdown(
        "### <img src='https://cdn-icons-png.flaticon.com/128/1041/1041888.png' width='40'> Dashboard Analisis",
        unsafe_allow_html=True,
    )
    render_stats_widgets()

elif menu == "Prediksi Churn":
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">',
        unsafe_allow_html=True,
    )
    st.markdown(
        '## <i class="fa-solid fa-microchip"></i> Analisis Risiko Churn',
        unsafe_allow_html=True,
    )
    st.markdown(
        "Masukkan data pelanggan di bawah ini untuk mendapatkan prediksi instan."
    )
    st.write("---")

    # Bungkus form untuk input data pelanggan
    with st.form("form_prediksi"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Umur", 18, 100, value=None, placeholder="Masukkan umur pelanggan"
            )
            sub_months = st.number_input(
                "Lama Berlangganan (Bulan)",
                1,
                72,
                value=None,
                placeholder="Masukkan lama berlangganan",
            )
            monthly_logins = st.number_input(
                "Rata-rata Login Bulanan",
                0,
                50,
                value=None,
                placeholder="Masukkan rata-rata login bulanan",
            )
            last_purchase = st.number_input(
                "Hari Sejak Pembelian Terakhir",
                0,
                365,
                value=None,
                placeholder="Masukkan hari sejak pembelian terakhir",
            )
            usage_time = st.number_input(
                "Waktu Penggunaan App (Menit)",
                0,
                5000,
                value=None,
                placeholder="Masukkan waktu penggunaan app",
            )
            monthly_spend = st.number_input(
                "Pengeluaran Bulanan (USD)",
                0,
                1000,
                value=None,
                placeholder="Masukkan pengeluaran bulanan",
            )
            discount_pct = st.number_input(
                "Persentase Diskon yang Digunakan",
                0,
                100,
                value=None,
                placeholder="Masukkan persentase diskon yang digunakan",
            )
            support_calls = st.number_input(
                "Jumlah Panggilan Dukungan",
                0,
                20,
                value=None,
                placeholder="Masukkan jumlah panggilan dukungan",
            )
            satisfaction = st.slider(
                "Skor Kepuasan (1-5)", 1, 5, value=1, help="Pilih Tingkat kepuasan"
            )
            contract_type = st.selectbox(
                "Jenis Kontrak",
                ["Monthly", "Quarterly", "Annual"],
                index=None,
                placeholder="Pilih jenis kontrak",
            )

        # Tombol untuk submit form
        submit_button = st.form_submit_button("Analisis Sekarang")
        with col2:
            st.markdown("### 📌 Petunjuk Pengisian")
            st.write("""
            - Pastikan semua kolom diisi dengan benar untuk mendapatkan hasil yang akurat.
            - Gunakan data aktual pelanggan untuk analisis yang lebih relevan.
            - Setelah menekan tombol, tunggu beberapa saat untuk melihat hasil prediksi dan analisis faktor penyebabnya.
            """)
    # Logika menampilkan hasil hanya setelah tombol submit ditekan
    if submit_button:
        required_fields = [
            age,
            sub_months,
            monthly_logins,
            last_purchase,
            usage_time,
            monthly_spend,
            discount_pct,
            support_calls,
            satisfaction,
            contract_type,
        ]
        if any(v is None for v in required_fields):
            st.warning("⚠️ Harap isi semua kolom yang diperlukan.")

        else:
            input_data = {
                "Age": age,
                "Subscription_Duration_Months": sub_months,
                "Monthly_Logins": monthly_logins,
                "Last_Purchase_Days_Ago": last_purchase,
                "App_Usage_Time_Min": usage_time,
                "Monthly_Spend": monthly_spend,
                "Discount_Usage_Percentage": discount_pct,
                "Customer_Support_Calls": support_calls,
                "Satisfaction_Score": satisfaction,
                "Contract_Type": contract_type,
            }

            try:
                with st.spinner("🤖 AI sedang menganalisis perilaku pelanggan..."):
                    hasil = predict_churn(input_data)

                st.write("---")
                st.subheader("📊 Hasil Analisis Prediksi")

                res_col1, res_col2 = st.columns([1, 2])

                with res_col1:
                    if hasil["Prediksi"] == 1:
                        st.error(f"### {hasil['Label']}")
                    else:
                        st.success(f"### {hasil['Label']}")

                    st.metric(
                        "Probabilitas Churn", f"{hasil['Probabilitas Churn']:.1%}"
                    )

                    risk_colors = {
                        "Critical Risk": "🔴",
                        "High Risk": "🟠",
                        "Medium Risk": "🟡",
                        "Low Risk": "🟢",
                    }
                    icon = risk_colors.get(hasil["Level Risiko"], "⚪")
                    st.markdown(f"**Level Risiko:** {icon} {hasil['Level Risiko']}")

                with res_col2:
                    st.subheader("🔍 Analisis Faktor Penyebab")
                    shap_values = hasil.get("Penjelasan SHAP", {})
                    if shap_values:
                        df_plot = pd.DataFrame(shap_values)
                        fig = px.bar(df_plot, x='Nilai SHAP', y='Faktor', orientation='h',
                                     color='Kategori', color_discrete_map={'risk': 'red', 'protective': 'green'})
                        st.plotly_chart(fig, use_container_width=True)
                        for item in shap_values:
                            if item["Kategori"] == "risk":
                                st.warning(f"⚠️ **{item['Faktor']}**")
                                st.markdown(f"**Dampak:** {item['Pengaruh']}")
                                st.info(f"💡 **Rekomendasi:** {item['Rekomendasi']}")
                            else:
                                st.success(f"✅ **{item['Faktor']}**")
                                st.markdown(f"**Dampak:** {item['Pengaruh']}")
                                st.info(f"💡 **Rekomendasi:** {item['Rekomendasi']}")
                    else:
                        st.info("Tidak ada faktor tambahan yang dapat ditampilkan.")

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses prediksi: {e}")

elif menu == "Tentang Aplikasi":
    st.subheader("ℹ️ Tentang Aplikasi")
    st.write("""
    Aplikasi ini dikembangkan oleh tim PJK-GM079 untuk mendemonstrasikan integrasi antara model
    Machine Learning (Random Forest/XGBoost) dengan antarmuka web Streamlit.

    **Teknologi yang digunakan:**
    * **Backend:** Python, Scikit-Learn, SHAP
    * **Frontend:** Streamlit
    * **Struktur:** Modular (Inference logic terpisah dari UI)
    """)
render_footer()
