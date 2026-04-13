import os
import logging
from logging.handlers import RotatingFileHandler

from app.config import LOG_DIR, LOG_FILE, LOG_ERROR_FILE


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s'
    )

    os.makedirs(LOG_DIR, exist_ok=True)


    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    info_log_path = os.path.join(LOG_DIR, LOG_FILE)
    info_handler = RotatingFileHandler(
        filename=info_log_path,
        maxBytes=20*1024*1024,
        backupCount=5,
        encoding='utf-8',
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    error_log_path = os.path.join(LOG_DIR, LOG_ERROR_FILE)
    error_handler = RotatingFileHandler(
        filename=error_log_path,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8',
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger