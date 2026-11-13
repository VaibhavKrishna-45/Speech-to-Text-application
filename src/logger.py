"""Centralized application logging."""
import logging
from logging.handlers import RotatingFileHandler

from .config import LOG_DIR, LOG_FILE


def get_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if not any(getattr(handler, "_speech_to_text_handler", False) for handler in logger.handlers):
        handler = RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
        handler._speech_to_text_handler = True
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)
    return logger
