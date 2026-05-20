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

    st.markdown("## 🤖 Prediksi Churn Pelanggan")

    tab_manual, tab_file = st.tabs(["✍️ Input Manual", "📁 Unggah File CSV"])
    with tab_manual:
        st.markdown("### 📌 Petunjuk Pengisian")
        st.write("""
            - Pastikan semua kolom diisi dengan benar untuk mendapatkan hasil yang akurat.
            - Gunakan data aktual pelanggan untuk analisis yang lebih relevan.
        """)

        with st.form("form_prediksi"):
            col1, space, col2 = st.columns([1, 0.05, 1])

            with col1:
                st.markdown("### 📝 Input Data Pelanggan")
                customer_name = st.text_input(
                    "Nama Pelanggan",
                    value="",
                    placeholder="Masukkan nama pelanggan"
                    )
                
                age = st.number_input(
                    "Usia", 18, 100,
                    value=None,
                    placeholder="Masukkan usia pelanggan"
                    )
                
                sub_months = st.number_input(
                    "Lama Berlangganan (Bulan)", 1, 72,
                    value=None,
                    placeholder="Masukkan lama berlangganan"
                    )
                
                monthly_logins = st.number_input(
                    "Frekuensi Login Bulanan", 0, 50,
                    value=None,
                    placeholder="Masukkan rata-rata login bulanan"
                    )
                
                last_purchase = st.number_input(
                    "Hari Sejak Pembelian Terakhir", 0, 365,
                    value=None,
                    placeholder="Masukkan transaksi pembelian terakhir"
                    )
                
                usage_time = st.number_input(
                    "Waktu Penggunaan App (Menit)", 0, 5000,
                    value=None,
                    placeholder="Masukkan waktu penggunaan app"
                    )
                
                monthly_spend = st.number_input(
                    "Pengeluaran Bulanan (Rupiah)", 0, 10000000,
                    value=None,
                    placeholder="Masukkan pengeluaran bulanan"
                    )
                
                discount_pct = st.number_input(
                    "Persentase Diskon yang Digunakan", 0, 100,
                    value=None,
                    placeholder="Masukkan persentase diskon yang digunakan"
                    )
                
                support_calls = st.number_input(
                    "Jumlah Panggilan Komplain", 0, 50,
                    value=None,
                    placeholder="Masukkan jumlah panggilan komplain"
                    )
                
                satisfaction = st.slider(
                    "Skor Kepuasan (1-5)", 1, 5,
                    value=1
                    )
                
                contract_type = st.selectbox(
                    "Jenis Kontrak", ["Monthly", "Annual"],
                    index=None,
                    placeholder="Pilih jenis kontrak"
                    )

                submit_button = st.form_submit_button("Analisis Sekarang")

            with space:
                st.markdown(
                    '<div style="border-left: 1px solid rgba(128,128,128,0.25); height: 850px; margin: auto;"></div>',
                    unsafe_allow_html=True)

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
                        contract_type
                    ]
                    
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
                            with st.spinner("🤖 AI sedang menganalisis perilaku pelanggan..."):
                                hasil = predict_churn(input_data)
                                save_prediction(customer_name, input_data, hasil)
                                st.toast("✅ Prediksi berhasil disimpan!")
                            
                            if hasil["Prediksi"] == 1: st.error(f"### {hasil['Label']}")
                            else: st.success(f"### {hasil['Label']}")
                            
                            st.metric("Probabilitas Churn", f"{hasil['Probabilitas Churn']:.1%}")
                            risk_colors = {
                                "Critical Risk": "🔴",
                                "High Risk": "🟠",
                                "Medium Risk": "🟡",
                                "Low Risk": "🟢"}
                            st.markdown(f"**Level Risiko:** {risk_colors.get(hasil['Level Risiko'], '⚪')} {hasil['Level Risiko']}")
                            
                            st.markdown("---")
                            st.subheader("🔍 Analisis Faktor Penyebab")
                            shap_values = hasil.get("Penjelasan SHAP", [])
                            if shap_values:
                                for item in shap_values:
                                    if item["Kategori"] == "risk":
                                        st.warning(f"⚠️ **{item['Faktor']}**\n\n**Dampak:** {item['Pengaruh']}\n\n💡 **Rekomendasi:** {item['Rekomendasi']}")
                                    else:
                                        st.success(f"✅ **{item['Faktor']}**\n\n**Dampak:** {item['Pengaruh']}\n\n💡 **Rekomendasi:** {item['Rekomendasi']}")
                            else:
                                st.info("Tidak ada faktor tambahan.")
                        except Exception as e:
                            st.error(f"Terjadi kesalahan: {e}")

    with tab_file:
        st.markdown("### 📁 Prediksi Massal via File CSV")
        st.write("Unggah file CSV berisi data pelanggan untuk melakukan prediksi churn secara massal.")

        with st.expander("📋 Lihat Struktur Format Kolom CSV"):
            st.code(
                "Nama_Pelanggan,"
                "Age,"
                "Subscription_Duration_Months,"
                "Monthly_Logins," 
                "Last_Purchase_Days_Ago,"
                "App_Usage_Time_Min,Monthly_Spend,"
                "Discount_Usage_Percentage,"
                "Customer_Support_Calls,"
                "Satisfaction_Score,"
                "Contract_Type")
            st.caption("Pastikan nama kolom sama persis seperti contoh di atas (sensitif huruf besar/kecil).")

        uploaded_file = st.file_uploader("Pilih Berkas CSV Anda", type=["csv"])

        if uploaded_file is not None:
            try:
                # Membaca file CSV yang diunggah
                input_df = pd.read_csv(uploaded_file)
                st.success(f"📂 Berhasil memuat {len(input_df)} data pelanggan.")

                # Tombol untuk mengeksekusi prediksi massal
                if st.button("🚀 Jalankan Prediksi Massal"):
                    progress_bar = st.progress(0)
                    hasil_bulk = []
                    
                    with st.spinner("🤖 AI sedang memproses seluruh data pelanggan..."):
                        for index, row in input_df.iterrows():

                            # Mengekstrak data setiap baris
                            customer_name_bulk = str(row.get("Nama_Pelanggan", f"Pelanggan {index+1}"))
                            
                            row_data = {
                                "Age": int(row["Age"]),
                                "Subscription_Duration_Months": int(row["Subscription_Duration_Months"]),
                                "Monthly_Logins": int(row["Monthly_Logins"]),
                                "Last_Purchase_Days_Ago": int(row["Last_Purchase_Days_Ago"]),
                                "App_Usage_Time_Min": int(row["App_Usage_Time_Min"]),
                                "Monthly_Spend": float(row["Monthly_Spend"]),
                                "Discount_Usage_Percentage": int(row["Discount_Usage_Percentage"]),
                                "Customer_Support_Calls": int(row["Customer_Support_Calls"]),
                                "Satisfaction_Score": int(row["Satisfaction_Score"]),
                                "Contract_Type": str(row["Contract_Type"]),
                            }
                            
                            # Mengirim data ke fungsi predict_churn
                            hasil_single = predict_churn(row_data)
                            
                            # Menyimpan hasil prediksi ke database
                            save_prediction(customer_name_bulk, row_data, hasil_single)
                            
                            # Menggabungkan informasi untuk tabel review
                            row_data["Nama_Pelanggan"] = customer_name_bulk
                            row_data["Hasil_Prediksi"] = hasil_single["Label"]
                            row_data["Probabilitas_Churn"] = f"{hasil_single['Probabilitas Churn']:.1%}"
                            row_data["Level_Risiko"] = hasil_single["Level Risiko"]
                            
                            hasil_bulk.append(row_data)
                            
                            # Update progress bar biar interaktif
                            progress_bar.progress((index + 1) / len(input_df))
                    
                    # Konversi hasil list menjadi dataframe display
                    df_hasil = pd.DataFrame(hasil_bulk)
                    
                    st.markdown("---")
                    st.subheader("📊 Hasil Prediksi Masal")
                    st.dataframe(df_hasil, use_container_width=True)
                    
                    # Ringkasan data hasil prediksi massal
                    total_churn = len(df_hasil[df_hasil["Hasil_Prediksi"].str.contains("Churn")])
                    st.info(f"💡 Ringkasan Analisis: **{total_churn}** dari **{len(df_hasil)}** pelanggan diprediksi akan Churn.")
                    
            except Exception as e:
                st.error(f"⚠️ Format file tidak sesuai atau terjadi error: {e}")
