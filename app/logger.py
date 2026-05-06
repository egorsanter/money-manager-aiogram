import os
import json
import logging
from logging.handlers import RotatingFileHandler

from app.config import LOG_DIR, LOG_FILE, LOG_ERROR_FILE


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            'time': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'file': record.filename,
            'line': record.lineno,
            'user_id': getattr(record, 'user_id', None),
        }

        if record.exc_info:
            log['exception'] = self.formatException(record.exc_info)

        return json.dumps(log, ensure_ascii=False)


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.hasHandlers():
        return logger
    
    formatter = JsonFormatter()

    os.makedirs(LOG_DIR, exist_ok=True)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    info_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=20 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8',
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    logger.addHandler(info_handler)

    error_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, LOG_ERROR_FILE),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8',
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger