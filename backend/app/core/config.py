import os
from dotenv import load_dotenv #type: ignore

load_dotenv()

# App Settings
APP_NAME = "Stock Predictor Backend"
ENV = os.getenv("ENV", "development")

# Database settings
DB_URL = os.getenv("DB_URL", "sqlite:///./test.db")

# API settings
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Logging paths (OPTIONAL - only if you want config to control this)
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")


