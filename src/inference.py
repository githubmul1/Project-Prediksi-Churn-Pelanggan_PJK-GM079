import joblib
import pandas as pd

from config import MODEL_PATH, PIPELINE_PATH

# load sekali saat startup
model = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)


# Fungsi untuk menentukan tingkat risiko churn
def churn_risk_label(probability: float):

    if probability >= 0.8:
        return "Critical Risk"
    elif probability >= 0.6:
        return "High Risk"
    elif probability >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"


# fungsi untuk melakukan prediksi churn
def predict_churn(data: dict):

    # merubah dict menjadi DataFrame
    df = pd.DataFrame([data])

    # preprocessing data dengan pipeline
    X = pipeline.transform(df)

    # prediction
    prediction = model.predict(X)[0]

    # kemungkinan churn
    probability = model.predict_proba(X)[0][1]

    # memberikan label berdasarkan prediksi agar lebih manusiawi
    label = "Churn" if prediction == 1 else "Not Churn"

    return {
        "prediction": int(prediction),
        "label": label,
        "probability_churn": round(float(probability), 3),
        "risk_level": churn_risk_label(probability),
    }
