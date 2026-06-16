# 📊 Sistem Prediksi Churn Pelanggan E-Commerce

Sistem aplikasi berbasis data (_data-driven application_) yang dirancang untuk membantu bisnis _e-commerce_ dalam memprediksi risiko _churn_ pelanggan (potensi berhenti berlangganan). Aplikasi ini mengintegrasikan model _Machine Learning_ dengan antarmuka web interaktif untuk memberikan analisis prediktif yang cepat, akurat, dan dapat dijelaskan (_explainable_).

---

## 📦 Petunjuk Running Aplikasi dari Scratch

1. Pastikan package python Conda telah terinstall
2. Dari direktori root ketik perintah berikut di terminal :

```Terminal
conda env create -f environment.yml # membuat conda environment dari .yml
mlflow ui # menjalankan mlflow secara default
python -m src.modelling # menjalankan modellling
python -m streamlit run frontend/streamlit_app.py # menjalankan streamlit

```

6. Browser akan membuka otomatis tautan aplikasi

---

## 🔗 Tautan aplikasi siap pakai

Klik https://matnaryo-churn.hf.space/

---

## 📎 Tautan model .pkl

Klik https://drive.google.com/file/d/1oMpuuOGV_wMW2ObNHUFJxr1dBwnD6sSo/view?usp=drive_link

---

## 👥 Anggota Tim Pengembangan PJK-GM079

| NO  | ID Pijak      | Nama                  | Email                             |
| :-- | :------------ | :-------------------- | :-------------------------------- |
| 1   | APC847D6Y0007 | Hervan Wandri         | evandrie13@gmail.com              |
| 2   | APC809D6Y0033 | Rohmat Sunaryo        | rohmat.sunaryo@gmail.com          |
| 3   | APC013D6Y0094 | Hafiz Satria          | azizanhafiz123@gmail.com          |
| 4   | APC223D6Y0256 | Mulya Adi Putra       | lptpmul1@gmail.com                |
| 5   | APC240D6X0093 | Ruth Anastasya Harefa | ruth.anastasya.h@mail.ukrim.ac.id |

---

## 🎯 Fitur Utama Aplikasi

1. **Dashboard Analisis (Halaman Utama)**
   - Menyajikan ringkasan eksekutif (_Key Performance Indicators_) secara _real-time_ seperti Total Prediksi, _Churn Rate_, Rata-Rata Probabilitas, dan Jumlah Pelanggan Risiko Tinggi.
   - Visualisasi interaktif menggunakan grafik tren garis, segmentasi tingkat risiko (Donut Chart), dan komparasi karakteristik berdasarkan jenis kontrak (Bar Chart).

2. **Prediksi Churn (Input Manual & Massal)**
   - **✍️ Input Manual:** Mengidentifikasi risiko _churn_ pelanggan tunggal secara _real-time_ dengan fitur formulir otomatis (_auto-reset_). Dilengkapi dengan penjelasan kontribusi fitur menggunakan **SHAP (Explainable AI)** dan rekomendasi tindakan mitigasi bisnis.
   - **📁 Unggah File CSV:** Mengakomodasi pemrosesan data dalam skala besar (_bulk prediction_). Pengguna dapat mengunduh _template_ CSV yang disediakan, mengisinya secara kolektif, dan mengunggahnya kembali untuk melihat hasil prediksi terstruktur dengan sistem navigasi halaman (_pagination_).

3. **📜 Riwayat Prediksi**
   - Menampilkan seluruh data histori hasil prediksi yang tersimpan di database dalam bentuk tabel dinamis.
   - Dilengkapi fitur filter adaptif berdasarkan tingkat risiko (_Low_, _Medium_, _High_, _Critical_) serta tombol ekspor untuk mengunduh kembali riwayat data ke dalam file eksternal.

4. **ℹ️ Tentang Aplikasi**
   - Transparansi dokumentasi teknis sistem yang memuat informasi spesifikasi dataset, pustaka pengembangan, dan metrik performa evaluasi model.

---

## 🤖 Statistik & Performa Model AI

Model dikembangkan menggunakan algoritma **Random Forest Regressor/Classifier** dan dilatih menggunakan basis data sebanyak **15.000 data pelanggan**. Berdasarkan hasil pengujian (_testing_), model berhasil mencapai performa sebagai berikut:

| Metrik Evaluasi           | Nilai Performa |
| :------------------------ | :------------- |
| **Akurasi (_Accuracy_)**  | 92.0%          |
| **Presisi (_Precision_)** | 57.3%          |
| **Recall**                | 64.5%          |
| **F1-Score**              | 60.7%          |
| **ROC AUC**               | 93.2%          |

---

## 🛠️ Arsitektur Teknologi (Tech Stack)

- **Bahasa Pemrograman:** Python (v3.11)
- **Antarmuka Pengguna (Frontend):** Streamlit
- **Pemrosesan & Model ML:** Scikit-learn, Pandas, NumPy
- **Interpretabilitas Model:** SHAP (_SHapley Additive exPlanations_)
- **Visualisasi Data:** Plotly, Matplotlib / Seaborn
- **Penyimpanan Data (Database):** SQLite (`database/churn.db`)
- **Pelacakan Eksperimen:** MLflow (Tracking Server)

---

## 📁 Struktur Direktori Proyek

Project-Prediksi-Churn-Pelanggan_PJK-GM079/
│
├── api
│ └── api.py
│
│
├── database/
│ └── ecommerce_customer_churn_data.csv
│
│
├── database/
│ └── churn.db
│
├── frontend/
│ └── assets/
│ │ └── style.css
│ └── components/
│ │ └── footer.py
│ │ └── navbar.py
│ └── views/
│ │ └── about.py
│ │ └── dashboard.py
│ │ └── history.py
│ │ └── prediction.py
│ ├── mlflow.db
│ └── streamlit_app.py
│
├── models/
│ └── churn_model.pkl
│
├── notebooks/
│ └── eda_xda.ipynb
│
│
├── src/
│ ├── explainer.py
│ ├── inferece.py
│ ├── metrics.json
│ └── modelling.py
│
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
└── link_kaggle.txt t

```

```
