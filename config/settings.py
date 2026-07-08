from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ==========================
# DATABASE
# ==========================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==========================
# PROJECT PATH
# ==========================
BASE_FOLDER = os.getenv("BASE_FOLDER")

# ==========================
# LOGGING
# ==========================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ==========================
# APPLICATION
# ==========================

APP_URL = os.getenv("APP_URL")
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
FRONTEND_PATH = os.getenv("FRONTEND_PATH")
BACKEND_PATH = os.getenv("BACKEND_PATH")