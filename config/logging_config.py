import logging
import os
from logging.handlers import RotatingFileHandler

from config.settings import LOG_LEVEL

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/pipeline.log"

logger = logging.getLogger("ecommerce_pipeline")
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

logging.getLogger("WDM").setLevel(logging.WARNING)