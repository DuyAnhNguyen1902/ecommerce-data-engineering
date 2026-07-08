import time
from selenium.webdriver.common.by import By

from config.settings import APP_URL
from config.logging_config import logger


def login(driver, email, password):
    logger.info("Opening login page")

    driver.get(APP_URL)
    time.sleep(2)

    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    time.sleep(1)

    driver.find_element(
        By.XPATH,
        "//button[@type='button' and @class='chakra-button css-7ewgda']"
    ).click()

    time.sleep(1)

    logger.info("Login clicked")