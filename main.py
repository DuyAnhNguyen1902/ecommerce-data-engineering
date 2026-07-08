from scraper.pipeline import run_scraper
from ingestion.load_raw import load_raw

from config.logging_config import logger


def run_pipeline():
    logger.info("=" * 60)
    logger.info("START PIPELINE")
    logger.info("=" * 60)

    try:
        run_scraper()

        load_raw()

        logger.info("PIPELINE SUCCESS")

    except Exception as e:

        logger.exception("PIPELINE FAILED")

        raise

    finally:

        logger.info("=" * 60)


if __name__ == "__main__":
    run_pipeline()