import os
import sys
import sqlite3
import importlib.util
from config import DB_PATH

database_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(database_dir, "../"))
config_path = os.path.join(root_dir, "config.py")

if os.path.exists(config_path):
    spec = importlib.util.spec_from_file_location("config_root", config_path)
    config_root = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_root)
    DB_PATH = config_root.DB_PATH
else:
    raise FileNotFoundError(f"config.py tidak ditemukan di {config_path}")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)
