import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import (
    BASE_DIR,
    LOG_DIR,
    LOG_ERROR_BACKUP_COUNT,
    LOG_ERROR_FILE,
    LOG_ERROR_MAX_BYTES,
    LOG_FILE,
    LOG_INFO_BACKUP_COUNT,
    LOG_INFO_MAX_BYTES,
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'time': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'file': record.filename,
            'line': record.lineno,
            'user_id': getattr(record, 'user_id', None),
        }

        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def _get_log_dir() -> Path:
    log_dir = Path(LOG_DIR)

    if log_dir.is_absolute():
        return log_dir

    return BASE_DIR / log_dir


def _create_stream_handler(formatter: logging.Formatter) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    return handler


def _create_file_handler(
    filename: str,
    level: int,
    max_bytes: int,
    backup_count: int,
    formatter: logging.Formatter,
) -> logging.Handler:
    handler = RotatingFileHandler(
        filename=filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8',
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def configure_logging() -> None:
    logger = logging.getLogger()

    if logger.handlers:
        return

    logger.setLevel(logging.DEBUG)

    formatter = JsonFormatter()
    log_dir = _get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    console_handler = _create_stream_handler(formatter)
    info_handler = _create_file_handler(
        filename=str(log_dir / LOG_FILE),
        level=logging.INFO,
        max_bytes=LOG_INFO_MAX_BYTES,
        backup_count=LOG_INFO_BACKUP_COUNT,
        formatter=formatter,
    )
    error_handler = _create_file_handler(
        filename=str(log_dir / LOG_ERROR_FILE),
        level=logging.ERROR,
        max_bytes=LOG_ERROR_MAX_BYTES,
        backup_count=LOG_ERROR_BACKUP_COUNT,
        formatter=formatter,
    )

    handlers = (console_handler, info_handler, error_handler)
    for handler in handlers:
        logger.addHandler(handler)


def setup_logger(name: str) -> logging.Logger:
    configure_logging()

    return logging.getLogger(name)
