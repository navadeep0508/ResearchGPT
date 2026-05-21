from dotenv import load_dotenv
import os


load_dotenv()

APP_NAME=os.getenv("APP_NAME")
DEBUG = os.getenv("DEBUG")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")
DATABASE_URL = os.getenv("DATABASE_URL")

