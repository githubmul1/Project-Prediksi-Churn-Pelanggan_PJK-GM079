import numpy as np
import shap

# Feature Map(Alih bahasa agar lebih manusiawi)
FEATURE_MAP = {
    "numeric__Age": "Usia pelanggan",
    "numeric__Subscription_Duration_Months": "Lama berlangganan (bulan)",
    "numeric__Monthly_Logins": "Frekuensi login bulanan",
    "numeric__Last_Purchase_Days_Ago": "Hari sejak transaksi terakhir",
    "numeric__App_Usage_Time_Min": "Durasi penggunaan aplikasi (menit)",
    "numeric__Monthly_Spend": "Pengeluaran bulanan",
    "numeric__Discount_Usage_Percentage": "Persentase penggunaan diskon",
    "numeric__Customer_Support_Calls": "Jumlah komplain ke customer service",
    "numeric__Satisfaction_Score": "Tingkat kepuasan pelanggan",
    "numeric__Contract_Type_Annual": "Kontrak tahunan",
    "numeric__Contract_Type_Monthly": "Kontrak bulanan",
}


# Fungsi untuk menjelaskan hasil SHAP dalam bahasa manusiawi
def explain_human(top_reasons):

    result = []

    for r in top_reasons:
        feature = r["feature"]
        impact = r["impact"]

        name = FEATURE_MAP.get(feature, feature)

        if impact > 0:
            direction = "meningkatkan risiko churn"
            category = "risk"
        else:
            direction = "menurunkan risiko churn"
            category = "safe"

        result.append(
            {
                "Faktor": name,
                "Pengaruh": direction,
                "Nilai SHAP": round(float(impact), 4),
                "Kategori": category,
            }
        )

    return result


# Fungsi untuk memberikan rekomendasi berdasarkan faktor yang mempengaruhi churn
def recommendation_engine(factor_name):

    mapping = {
        "Jumlah komplain ke customer service": "Percepat respon CS + analisis akar masalah pelanggan",
        "Tingkat kepuasan pelanggan": "Lakukan survei kepuasan dan perbaiki UX aplikasi",
        "Frekuensi login bulanan": "Tingkatkan engagement (push notification / gamification)",
        "Hari sejak transaksi terakhir": "Kirim campaign re-engagement / promo win-back",
        "Pengeluaran bulanan": "Buat personalisasi penawaran untuk meningkatkan spending",
        "Persentase penggunaan diskon": "Optimalkan strategi loyalty & diskon berulang",
        "Lama berlangganan (bulan)": "Berikan reward pelanggan jangka panjang (loyalty program)",
    }

    return mapping.get(factor_name, "Perlu analisis lebih lanjut")


# Fungsi untuk menjelaskan hasil churn
def explain_churn(X, feature_names, explainer, top_n=3):

    shap_values = explainer(X)

    values = shap_values.values

    # menangani bentuk SHAP
    if len(values.shape) == 3:
        # multiclass / binary probabilistic
        values = values[0, :, -1]
    elif len(values.shape) == 2:
        values = values[0]

    idx = np.argsort(np.abs(values))[::-1][:top_n]

    explanation = []

    for i in idx:
        explanation.append(
            {
                "feature": feature_names[i],
                "impact": float(
                    values[i].item() if hasattr(values[i], "item") else values[i]
                ),
            }
        )

    return explanation


# Fungsi untuk menghasilkan penjelasan akhir
def generate_explanation(top_reasons):

    human = explain_human(top_reasons)

    for item in human:
        item["Rekomendasi"] = recommendation_engine(item["Faktor"])

    return human
