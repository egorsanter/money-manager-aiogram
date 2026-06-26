import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise RuntimeError(
        'BOT_TOKEN is missing. Create a .env file based on .env.example'
    )

LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.getenv('LOG_FILE', 'bot_info.log')
LOG_ERROR_FILE = os.getenv('LOG_ERROR_FILE', 'bot_error.log')
LOG_INFO_MAX_BYTES = 20 * 1024 * 1024
LOG_INFO_BACKUP_COUNT = 5
LOG_ERROR_MAX_BYTES = 5 * 1024 * 1024
LOG_ERROR_BACKUP_COUNT = 3

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError(
        'DATABASE_URL is missing. Create a .env file based on .env.example'
    )
