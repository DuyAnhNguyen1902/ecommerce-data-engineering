import os
import subprocess
import time

from config.settings import FRONTEND_PATH, BACKEND_PATH
from config.logging_config import logger


def get_creation_flags():
    if os.name == "nt":
        return subprocess.CREATE_NO_WINDOW
    return 0


def start_frontend():
    logger.info("Starting React frontend")

    subprocess.Popen(
        "npm start",
        cwd=FRONTEND_PATH,
        shell=True,
        creationflags=get_creation_flags()
    )

    logger.info("React frontend started")
    time.sleep(10)


def start_backend():
    logger.info("Starting Spring Boot backend")

    subprocess.Popen(
        "cmd /c .\\mvnw spring-boot:run" if os.name == "nt" else "./mvnw spring-boot:run",
        cwd=BACKEND_PATH,
        shell=True,
        creationflags=get_creation_flags()
    )

    logger.info("Spring Boot backend started")
    time.sleep(10)


def start_application():
    start_frontend()
    start_backend()