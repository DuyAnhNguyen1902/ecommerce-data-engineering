import os
import time
from zipfile import BadZipFile, ZipFile

import pandas as pd

from config.logging_config import logger
from config.settings import (
    BASE_FOLDER,
    EXCEL_FILE_MAX_RETRIES,
    EXCEL_FILE_RETRY_DELAY_SECONDS,
)
from ingestion.raw_schema import (
    RAW_TABLE_SCHEMAS,
    normalize_and_validate_dataframe,
    normalize_identifier,
)


class ExcelReader:
    def __init__(
        self,
        folder_path=BASE_FOLDER,
        max_retries=EXCEL_FILE_MAX_RETRIES,
        retry_delay_seconds=EXCEL_FILE_RETRY_DELAY_SECONDS,
    ):
        if not folder_path:
            raise ValueError(
                "BASE_FOLDER must point to the Excel export directory."
            )

        if max_retries < 1:
            raise ValueError("max_retries must be at least 1.")

        if retry_delay_seconds < 0:
            raise ValueError(
                "retry_delay_seconds cannot be negative."
            )

        self.folder_path = folder_path
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    @staticmethod
    def is_file_ready(file_path):
        try:
            with open(file_path, "rb") as file:
                with ZipFile(file) as workbook:
                    return "[Content_Types].xml" in workbook.namelist()
        except (OSError, BadZipFile):
            return False

    def get_latest_excel_file(self):
        if not os.path.isdir(self.folder_path):
            raise FileNotFoundError(
                f"Excel folder does not exist: {self.folder_path}"
            )

        files = [
            os.path.join(self.folder_path, file_name)
            for file_name in os.listdir(self.folder_path)
            if file_name.lower().endswith(".xlsx")
            and not file_name.startswith("~$")
        ]

        if not files:
            raise FileNotFoundError(
                f"No valid Excel file found in: {self.folder_path}"
            )

        latest_file = max(files, key=os.path.getctime)

        for attempt in range(1, self.max_retries + 1):
            if self.is_file_ready(latest_file):
                logger.info(
                    "Excel file is ready | file=%s",
                    latest_file,
                )
                return latest_file

            logger.warning(
                "Excel file is not ready | file=%s | attempt=%s/%s",
                latest_file,
                attempt,
                self.max_retries,
            )

            if attempt < self.max_retries:
                time.sleep(self.retry_delay_seconds)

        waited_seconds = (
            self.max_retries - 1
        ) * self.retry_delay_seconds

        raise TimeoutError(
            f"Excel file remained unavailable after "
            f"{self.max_retries} attempts "
            f"({waited_seconds:.1f} seconds): {latest_file}"
        )

    def read_latest_file(self):
        latest_file = self.get_latest_excel_file()
        sheet_data = {}

        with pd.ExcelFile(latest_file) as workbook:
            for sheet_name in workbook.sheet_names:
                table_name = normalize_identifier(sheet_name)

                if table_name not in RAW_TABLE_SCHEMAS:
                    logger.info(
                        "Skipping non-source Excel sheet | sheet=%s",
                        sheet_name,
                    )
                    continue

                dataframe = workbook.parse(sheet_name)

                if dataframe.empty:
                    logger.warning(
                        "Skipping empty source sheet | sheet=%s",
                        sheet_name,
                    )
                    continue

                sheet_data.setdefault(table_name, []).append(
                    dataframe
                )

        missing_tables = sorted(
            set(RAW_TABLE_SCHEMAS) - set(sheet_data)
        )

        if missing_tables:
            raise ValueError(
                "Excel export is missing required source sheets: "
                f"{missing_tables}"
            )

        final_tables = {}

        for table_name, dataframes in sheet_data.items():
            combined_dataframe = pd.concat(
                dataframes,
                ignore_index=True,
            )

            final_tables[table_name] = (
                normalize_and_validate_dataframe(
                    combined_dataframe,
                    table_name,
                )
            )

        logger.info(
            "Excel file read successfully | file=%s | tables=%s",
            latest_file,
            len(final_tables),
        )

        return final_tables