from pathlib import Path

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

# path file
API_PATH = API_DIR / "api.py"
MODEL_PATH = MODELS_DIR / "churn_model.pkl"
