# ==========================================
# IMPORT LIBRARY
# ==========================================
import os
import joblib
import mlflow
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from config import DATA_DIR, MODEL_PATH

# ==========================================
# MLFLOW
# ==========================================
mlflow.set_tracking_uri("http://127.0.0.1:5000/")
mlflow.set_experiment("Churn Prediction")


# ==========================================
# LOAD RAW DATA
# ==========================================
data = pd.read_csv(os.path.join(DATA_DIR, "ecommerce_customer_churn_data.csv"))

print(data.head())

# ==========================================
# TARGET & FEATURE
# ==========================================
X = data.drop("Is_Churn", axis=1)
y = data["Is_Churn"]

# ==========================================
# SPLIT DATA
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42,
)

# ==========================================
# KOLOM NUMERIK & KATEGORIK
# ==========================================
numerical_columns = [
    "Age",
    "Subscription_Duration_Months",
    "Monthly_Logins",
    "Last_Purchase_Days_Ago",
    "App_Usage_Time_Min",
    "Monthly_Spend",
    "Discount_Usage_Percentage",
    "Customer_Support_Calls",
    "Satisfaction_Score",
]

categorical_columns = ["Contract_Type"]

# ==========================================
# PREPROCESSING NUMERIK
# ==========================================
numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

# ==========================================
# PREPROCESSING KATEGORIK
# ==========================================
categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

# ==========================================
# COLUMN TRANSFORMER
# ==========================================
preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_transformer,
            numerical_columns,
        ),
        (
            "categoric",
            categorical_transformer,
            categorical_columns,
        ),
    ]
)


# ==========================================
# FULL PIPELINE
# ==========================================
full_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "model",
            RandomForestClassifier(
                n_estimators=150,
                max_depth=15,
                min_samples_split=10,
                class_weight="balanced",
                n_jobs=1,
                random_state=42,
            ),
        ),
    ]
)

# ==========================================
# THRESHOLD
# ==========================================
threshold = 0.4

# ==========================================
# TRAINING
# ==========================================
with mlflow.start_run():
    mlflow.autolog()

    # train pipeline
    full_pipeline.fit(X_train, y_train)

    # probabilitas
    y_proba = full_pipeline.predict_proba(X_test)[:, 1]

    # thresholding
    y_pred = (y_proba >= threshold).astype(int)

    # metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    # logging
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("roc_auc", roc_auc)
    mlflow.log_param("threshold", threshold)

    # save mlflow model
    mlflow.sklearn.log_model(
        sk_model=full_pipeline,
        artifact_path="model",
        input_example=X_train.iloc[0:5],
    )

    # save joblib
    joblib.dump(full_pipeline, MODEL_PATH)

# ==========================================
# OUTPUT
# ==========================================
print("\nModel berhasil disimpan")
print(f"Path : {MODEL_PATH}")
print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC AUC  : {roc_auc:.4f}")
