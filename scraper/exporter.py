import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.logging_config import logger


def export_excel(driver):
    wait = WebDriverWait(driver, 20)

    logger.info("Waiting for Select All button")

    select_all_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Select All')]")
        )
    )

    select_all_btn.click()
    logger.info("Clicked Select All")

    export_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Export Excel')]")
        )
    )

    export_btn.click()
    logger.info("Clicked Export Excel")

    time.sleep(10)

    logger.info("Excel export completed")