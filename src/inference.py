import joblib
import pandas as pd
import shap

from datetime import datetime

try:
    import shap
except ImportError:
    shap = None

from config import MODEL_PATH
from src.explainer import explain_churn, generate_explanation

# =========================
# LOAD FULL PIPELINE
# =========================
model = joblib.load(MODEL_PATH)
preprocessor = model.named_steps["preprocessor"]
rf_model = model.named_steps["model"]

if shap is not None:
    explainer = shap.Explainer(rf_model) if shap is not None else None
else:
    explainer = None


# =========================
# LABEL RISIKO
# =========================
def churn_risk_label(probability: float):

    if probability >= 0.8:
        return "Critical Risk"

    elif probability >= 0.6:
        return "High Risk"

    elif probability >= 0.4:
        return "Medium Risk"

    else:
        return "Low Risk"


# =========================
# PREDIKSI CHURN
# =========================
def predict_churn(data: dict):

    # -------------------------
    # INPUT USER -> DATAFRAME
    # -------------------------
    df = pd.DataFrame([data])

    # -------------------------
    # PREDIKSI FULL PIPELINE
    # -------------------------
    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0][1]

    label = "Churn" if prediction == 1 else "Not Churn"

    # -------------------------
    # PREPROCESS UNTUK SHAP
    # -------------------------
    X_processed = preprocessor.transform(df)

    # jika sparse matrix
    if hasattr(X_processed, "toarray"):
        X_processed = X_processed.toarray()

    # -------------------------
    # FEATURE NAMES
    # -------------------------
    feature_names = preprocessor.get_feature_names_out()

    # -------------------------
    # SHAP EXPLANATION
    # -------------------------
    explanation = explain_churn(X_processed, feature_names, explainer)

    # -------------------------
    # RETURN RESULT
    # -------------------------
    return {
        "Prediksi": int(prediction),
        "Label": label,
        "Probabilitas Churn": round(float(probability), 3),
        "Level Risiko": churn_risk_label(probability),
        "Penjelasan SHAP": generate_explanation(explanation),
        "Timestamp": datetime.now().isoformat(),
    }
