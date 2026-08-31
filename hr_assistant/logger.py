import logging
import os
from datetime import datetime


LOGS_DIR = "logs"

_today = datetime.now().strftime("%Y-%m-%d")
DAILY_LOG_DIR = os.path.join(LOGS_DIR, _today)

os.makedirs(DAILY_LOG_DIR, exist_ok=True)

_run_started_at = datetime.now().strftime("%Y-%m-%d-%H%M%S")
LOG_FILE = os.path.join(DAILY_LOG_DIR, f"{_run_started_at}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)