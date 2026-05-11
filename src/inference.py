import joblib
import pandas as pd
import shap
from datetime import datetime

from config import MODEL_PATH, PIPELINE_PATH
from src.explainer import explain_churn, generate_explanation

# Load model and pipeline
model = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)

explainer = shap.Explainer(model)


# Fungsi untuk menentukan label risiko churn
def churn_risk_label(probability: float):

    if probability >= 0.8:
        return "Critical Risk"
    elif probability >= 0.6:
        return "High Risk"
    elif probability >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"


# Fungsi untuk memprediksi risiko churn
def predict_churn(data: dict):

    df = pd.DataFrame([data])

    X = pipeline.transform(df)

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]

    label = "Churn" if prediction == 1 else "Not Churn"

    # ekstraksi nama fitur
    try:
        feature_names = pipeline.get_feature_names_out()
    except:
        feature_names = df.columns

    # Penjelasan dengan library SHAP
    explanation = explain_churn(X, feature_names, explainer)

    # Kembalikan nilai dan tampilkan
    return {
        "Prediksi": int(prediction),
        "Label": label,
        "Probabilitas Churn": round(float(probability), 3),
        "Level Risiko": churn_risk_label(probability),
        "Penjelasan SHAP": generate_explanation(explanation),
        "Timestamp": datetime.now().isoformat(),
    }
