import logging
import os
from datetime import datetime


LOGS_DIR= "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

#everytime we run app.py, a new log file will be created
#until and unless terminated

_run_started_at= datetime.now().strftime("%Y-%m-%d-%H%M%S")
LOG_FILE= os.path.join(LOGS_DIR, f"{_run_started_at}.log")

logging.basicConfig(
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers= [
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def get_logger(name: str)-> logging.Logger:
    return logging.getLogger(name) 