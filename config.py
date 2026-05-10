from pathlib import Path

from regex import D

# direktori utama project
BASE_DIR = Path(__file__).resolve().parent

# direktori umum
API_DIR = BASE_DIR / "api"
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"
FRONTEND_DIR = BASE_DIR / "frontend"
MODELS_DIR = BASE_DIR / "models"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SRC_DIR = BASE_DIR / "src"

# file model
API_PATH = API_DIR / "api.py"
DATA_RAW_PATH = DATA_DIR / "raw/ecommerce_customer_churn.csv"
MODEL_PATH = MODELS_DIR / "churn_model.pkl"
PIPELINE_PATH = MODELS_DIR / "preprocessing_pipeline.pkl"
