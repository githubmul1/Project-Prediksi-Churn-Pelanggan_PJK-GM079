from fastapi import FastAPI
from pydantic import BaseModel

# import fungsi dari inference.py
from src.inference import predict_churn

# tautkan app dari backend FastAPI
app = FastAPI(
    title="Customer Churn Prediction API",
    description="API untuk prediksi churn pelanggan menggunakan machine learning",
    version="1.0.0",
)


# Halaman root dari app FastAPI
@app.get("/")
def home():
    return {"message": "API aktif"}


# membuat class untuk data customer
class CustomerData(BaseModel):
    Age: int
    Subscription_Duration_Months: int
    Monthly_Logins: int
    Last_Purchase_Days_Ago: int
    App_Usage_Time_Min: float
    Monthly_Spend: float
    Discount_Usage_Percentage: float
    Customer_Support_Calls: int
    Satisfaction_Score: int
    Contract_Type: str


# post endpoint untuk prediksi churn
@app.post(
    "/predict",
    summary="Prediksi churn customer",
    description="Menerima data customer dan menghasilkan prediksi churn",
)
# membuat fungsi untuk menangani request prediksi
def predict(data: CustomerData):

    result = predict_churn(data.model_dump())

    return result
