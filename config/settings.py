import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# PostgreSQL
# ==========================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5433))
DB_NAME = os.getenv("DB_NAME", "ecommerce_dw")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==========================
# Folder
# ==========================
BASE_FOLDER = os.getenv("BASE_FOLDER")

# ==========================
# Logging
# ==========================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==========================
# Trendify App
# ==========================
APP_URL = os.getenv("APP_URL")
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")

# ==========================
# Local App Paths
# ==========================
FRONTEND_PATH = os.getenv("FRONTEND_PATH")
BACKEND_PATH = os.getenv("BACKEND_PATH")

# ==========================
# Docker / Services
# ==========================
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce_dw")

PGADMIN_EMAIL = os.getenv("PGADMIN_EMAIL")
PGADMIN_PASSWORD = os.getenv("PGADMIN_PASSWORD")

AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "admin")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")