import subprocess
import time

from config.settings import FRONTEND_PATH, BACKEND_PATH
from config.logging_config import logger


def start_frontend():
    logger.info("Starting React frontend")

    subprocess.Popen(
        "npm start",
        cwd=FRONTEND_PATH,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    logger.info("React frontend started")
    time.sleep(10)


def start_backend():
    logger.info("Starting Spring Boot backend")

    subprocess.Popen(
        "cmd /c .\\mvnw spring-boot:run",
        cwd=BACKEND_PATH,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    logger.info("Spring Boot backend started")
    time.sleep(10)


def start_application():
    start_frontend()
    start_backend()