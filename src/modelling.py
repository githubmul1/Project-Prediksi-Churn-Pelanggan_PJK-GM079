import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
import numpy as np
import os
import joblib

mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("Churn Prediction")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "")

data = pd.read_csv(os.path.join(MODEL_DIR, "../data/processed/train_processed.csv"))

X = data.drop("Is_Churn", axis=1)
y = data["Is_Churn"]

# Subsampling + stratify
X_small, _, y_small, _ = train_test_split(
    X, y, train_size=0.9, stratify=y, random_state=42
)

# Split train-test
X_train, X_test, y_train, y_test = train_test_split(
    X_small, y_small, test_size=0.2, stratify=y_small, random_state=42
)

input_example = X_train.iloc[0:5]

# Model
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_split=10,
    class_weight="balanced",
    n_jobs=1,
    random_state=42,
)

# Threshold sudah di tuned
threshold = 0.4

with mlflow.start_run():
    mlflow.autolog()

    # Train
    model.fit(X_train, y_train)

    # Probabilitas
    y_proba = model.predict_proba(X_test)[:, 1]

    # Apply threshold
    y_pred = (y_proba >= threshold).astype(int)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    # Logging ke MLflow
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("roc_auc", roc_auc)
    mlflow.log_param("threshold", threshold)

    # Simpan model
    mlflow.sklearn.log_model(
        sk_model=model, artifact_path="model", input_example=input_example
    )

    # Path file model
    model_path = os.path.join(MODEL_DIR, "../models/churn_model.pkl")

    # Simpan
    joblib.dump(model, model_path)

print(f"Model disimpan di: {model_path}")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC AUC  : {roc_auc:.4f}")
