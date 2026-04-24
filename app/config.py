import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Create a .env file based on .env.example")

LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.getenv('LOG_FILE', 'bot_info.log')
LOG_ERROR_FILE = os.getenv('LOG_ERROR_FILE', 'bot_error.log')

DATABASE_URL = os.getenv('DATABASE_URL')