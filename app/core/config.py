from dotenv import load_dotenv
import os


load_dotenv()

APP_NAME = os.getenv("APP_NAME", "ResearchGPT")
DEBUG = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN:
    HF_TOKEN = HF_TOKEN.strip('"').strip("'")
HF_MODEL = os.getenv("HF_MODEL", "meta-llama/Llama-3.1-8B-Instruct")
if HF_MODEL:
    HF_MODEL = HF_MODEL.strip('"').strip("'")
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.strip('"').strip("'")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
if SECRET_KEY:
    SECRET_KEY = SECRET_KEY.strip('"').strip("'")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
