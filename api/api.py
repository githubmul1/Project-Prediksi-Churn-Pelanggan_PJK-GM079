from fastapi import FastAPI
from pydantic import BaseModel

# mengimport fungsi dari inference.py
from src.inference import predict_churn

# tautkan app dari backend FastAPI
# Bagian ini berisi informasi dasar API seperti nama, deskripsi, dan versi
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


# endpoint ini dipakai buat nerima data customer lalu diprediksi apakah churn atau tidak
# Endpoint ini menerima data customer lalu memproses prediksi
@app.post(
    "/predict",
    summary="Prediksi churn customer",
    description="Menerima data customer dan menghasilkan prediksi churn",
)
# membuat Fungsi predict() yang akan dijalankan ketika endpoint /predict dipanggil
def predict(data: CustomerData):
    # data dari user diubah dulu ke bentuk dictionary supaya bisa dibaca model
    result = predict_churn(data.model_dump())

    return result
