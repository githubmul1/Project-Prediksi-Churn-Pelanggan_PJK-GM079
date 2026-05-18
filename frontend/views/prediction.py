import os
import sys
import pandas as pd
import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from database.save_output import save_prediction
from src.inference import predict_churn


def render_prediction():
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">',
        unsafe_allow_html=True,
    )

    st.markdown("### 📌 Petunjuk Pengisian")
    st.write("""
        - Pastikan semua kolom diisi dengan benar untuk mendapatkan hasil yang akurat.
        - Gunakan data aktual pelanggan untuk analisis yang lebih relevan.
        - Setelah menekan tombol, tunggu beberapa saat untuk melihat hasil prediksi dan analisis faktor penyebabnya.
    """)

    st.markdown(
        "Masukkan data pelanggan di bawah ini untuk mendapatkan prediksi instan."
    )

    # Bungkus form untuk input data pelanggan
    with st.form("form_prediksi"):
        col1, space, col2 = st.columns([1, 0.05, 1])

        with col1:
            st.markdown("### 📝 Input Data Pelanggan")
            customer_name = st.text_input(
                "Nama Pelanggan", value="", placeholder="Masukkan nama pelanggan"
            )
            age = st.number_input(
                "Usia", 18, 100, value=None, placeholder="Masukkan usia pelanggan"
            )
            sub_months = st.number_input(
                "Lama Berlangganan (Bulan)",
                1,
                72,
                value=None,
                placeholder="Masukkan lama berlangganan",
            )
            monthly_logins = st.number_input(
                "Frekuensi Login Bulanan",
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
                placeholder="Masukkan transaksi pembelian terakhir",
            )
            usage_time = st.number_input(
                "Waktu Penggunaan App (Menit)",
                0,
                5000,
                value=None,
                placeholder="Masukkan waktu penggunaan app",
            )
            monthly_spend = st.number_input(
                "Pengeluaran Bulanan (Rupiah)",
                0,
                10000000,
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
                "Jumlah Panggilan Komplain",
                0,
                50,
                value=None,
                placeholder="Masukkan jumlah panggilan komplain ke customer service",
            )
            satisfaction = st.slider(
                "Skor Kepuasan (1-5)", 1, 5, value=1, help="Pilih Tingkat kepuasan"
            )
            contract_type = st.selectbox(
                "Jenis Kontrak",
                ["Monthly", "Annual"],
                index=None,
                placeholder="Pilih jenis kontrak",
            )

            # Tombol submit button untuk menjalankan prediksi
            submit_button = st.form_submit_button("Analisis Sekarang")

        # Tambahkan garis vertikal sebagai pemisah dengan space kecil di antaranya
        with space:
            st.markdown(
                """
                <div style="
                    border-left: 1px solid rgba(128,128,128,0.25);
                    height: 1000px;
                    margin: auto;
                "></div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.subheader("📊 Hasil Analisis Prediksi")
            if submit_button:
                required_fields = [
                    customer_name,
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
                # Validasi input
                if any(v is None for v in required_fields):
                    st.warning("⚠️ Harap isi semua kolom yang diperlukan.")
                elif not customer_name.replace(" ", "").isalpha():
                    st.warning("⚠️ Nama pelanggan harus berupa huruf.")
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
                        with st.spinner(
                            "🤖 AI sedang menganalisis perilaku pelanggan..."
                        ):
                            hasil = predict_churn(input_data)
                            try:
                                save_prediction(customer_name, input_data, hasil)
                                st.toast("✅ Prediksi berhasil disimpan ke database!")
                            except Exception as e:
                                st.error(
                                    f"⚠️ Gagal menyimpan prediksi ke database: {e}"
                                )

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

                        # Analisis Faktor Penyebab
                        st.markdown("---")
                        st.subheader("🔍 Analisis Faktor Penyebab")

                        # Penjelasan SHAP
                        shap_values = hasil.get("Penjelasan SHAP", [])
                        if shap_values:
                            df_plot = pd.DataFrame(shap_values)

                            for item in shap_values:
                                if item["Kategori"] == "risk":
                                    st.warning(f"⚠️ **{item['Faktor']}**")
                                    st.markdown(f"**Dampak:** {item['Pengaruh']}")
                                    st.info(
                                        f"💡 **Rekomendasi:** {item['Rekomendasi']}"
                                    )
                                else:
                                    st.success(f"✅ **{item['Faktor']}**")
                                    st.markdown(f"**Dampak:** {item['Pengaruh']}")
                                    st.info(
                                        f"💡 **Rekomendasi:** {item['Rekomendasi']}"
                                    )
                        else:
                            st.info("Tidak ada faktor tambahan yang dapat ditampilkan.")

                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat memproses prediksi: {e}")
