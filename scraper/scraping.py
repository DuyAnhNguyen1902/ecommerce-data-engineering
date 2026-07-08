from scraper.server import start_application
from scraper.driver import create_driver
from scraper.login import login
from scraper.exporter import export_excel

from config.settings import LOGIN_EMAIL, LOGIN_PASSWORD
from config.logging_config import logger


def run_scraper():
    logger.info("Scraper pipeline started")

    start_application()

    driver = create_driver()

    try:
        login(driver, LOGIN_EMAIL, LOGIN_PASSWORD)
        export_excel(driver)

        logger.info("Scraper pipeline completed")

    finally:
        driver.quit()
        logger.info("Chrome driver closed")


if __name__ == "__main__":
    run_scraper()