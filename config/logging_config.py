import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import LOG_LEVEL


LOGGER_NAME = "ecommerce_pipeline"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIRECTORY = Path(
    os.getenv("LOG_DIRECTORY", PROJECT_ROOT / "logs")
)
LOG_FILE = LOG_DIRECTORY / "pipeline.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

level_name = str(LOG_LEVEL).strip().upper()
log_level = getattr(logging, level_name, logging.INFO)

formatter = logging.Formatter(LOG_FORMAT)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(log_level)
logger.propagate = False


def has_managed_handler(handler_type):
    return any(
        isinstance(handler, handler_type)
        and getattr(handler, "_ecommerce_handler", False)
        for handler in logger.handlers
    )


def configure_console_handler():
    if has_managed_handler(logging.StreamHandler):
        return

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    console_handler._ecommerce_handler = True

    logger.addHandler(console_handler)


def configure_file_handler():
    if has_managed_handler(RotatingFileHandler):
        return

    try:
        LOG_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        file_handler._ecommerce_handler = True

        logger.addHandler(file_handler)

    except OSError as error:
        logger.warning(
            "File logging could not be configured | "
            "file=%s | error=%s",
            LOG_FILE,
            error,
        )


configure_console_handler()
configure_file_handler()

# Reduce unnecessary logs from WebDriver Manager.
logging.getLogger("WDM").setLevel(logging.WARNING)