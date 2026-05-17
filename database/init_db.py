from database.connect_db import get_connection


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        name TEXT,
        age INTEGER,
        subscription_duration_months INTEGER,
        monthly_logins INTEGER,
        last_purchase_days_ago INTEGER,
        app_usage_time_min INTEGER,
        monthly_spend REAL,
        discount_usage_percentage REAL,
        customer_support_calls INTEGER,
        satisfaction_score INTEGER,
        contract_type TEXT,
        prediction INTEGER,
        label TEXT,
        churn_probability REAL,
        risk_level TEXT
    )
    """)

    conn.commit()
    conn.close()
