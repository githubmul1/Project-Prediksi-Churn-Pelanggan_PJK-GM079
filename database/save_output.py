import json
from datetime import datetime

from database.connect_db import get_connection


def save_prediction(name, input_data, hasil):

    conn = get_connection()

    conn.execute(
        """
    INSERT INTO predictions (
        timestamp,
        name,
        age,
        subscription_duration_months,
        monthly_logins,
        last_purchase_days_ago,
        app_usage_time_min,
        monthly_spend,
        discount_usage_percentage,
        customer_support_calls,
        satisfaction_score,
        contract_type,
        prediction,
        churn_probability,
        risk_level
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            datetime.now().isoformat(),
            name,
            input_data["Age"],
            input_data["Subscription_Duration_Months"],
            input_data["Monthly_Logins"],
            input_data["Last_Purchase_Days_Ago"],
            input_data["App_Usage_Time_Min"],
            input_data["Monthly_Spend"],
            input_data["Discount_Usage_Percentage"],
            input_data["Customer_Support_Calls"],
            input_data["Satisfaction_Score"],
            input_data["Contract_Type"],
            hasil["Prediksi"],
            hasil["Probabilitas Churn"],
            hasil["Level Risiko"],
        ),
    )
    conn.commit()
    conn.close()


def get_all_predictions():

    conn = get_connection()

    cursor = conn.execute("""
    SELECT *
    FROM predictions
    ORDER BY id DESC
    """)
    print(cursor.lastrowid)
    rows = cursor.fetchall()

    conn.close()

    return rows
