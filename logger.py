"""
logger.py
---------
Centralized logging configuration for the CareerIQ application.
All modules import from here to ensure consistent log formatting.
"""

import logging
import os
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    Logs to both console and a file in the logs/ directory.

    Args:
        name: Usually __name__ from the calling module.

    Returns:
        logging.Logger: Configured logger instance.
    """

    # Ensure logs directory exists
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    logger = logging.getLogger(name)

    # Prevent duplicate handlers (important for Streamlit reruns)
    if logger.handlers:
        return logger

    logger.setLevel(log_level)
    logger.propagate = False  # prevent duplicate logs

    # Log format
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        log_dir / "app.log",
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger