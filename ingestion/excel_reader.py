import os
import time
import pandas as pd

from config.settings import BASE_FOLDER


class ExcelReader:
    def __init__(self, folder_path=BASE_FOLDER):
        self.folder_path = folder_path

    def is_file_ready(self, file_path):
        try:
            with open(file_path, "rb"):
                return True
        except Exception:
            return False

    def get_latest_excel_file(self):
        files = [
            os.path.join(self.folder_path, f)
            for f in os.listdir(self.folder_path)
            if f.endswith(".xlsx") and not f.startswith("~$")
        ]

        if not files:
            raise FileNotFoundError("No valid Excel file found.")

        latest_file = max(files, key=os.path.getctime)

        while not self.is_file_ready(latest_file):
            print("Waiting file release...")
            time.sleep(1)

        return latest_file

    def read_latest_file(self):
        latest_file = self.get_latest_excel_file()

        print(f"Using file: {latest_file}")

        sheet_data = {}
        xls = pd.ExcelFile(latest_file)

        for sheet in xls.sheet_names:
            df = xls.parse(sheet)

            if df.empty:
                continue

            table_name = sheet.strip().lower().replace(" ", "_")

            if table_name not in sheet_data:
                sheet_data[table_name] = []

            sheet_data[table_name].append(df)

        final_tables = {}

        for table_name, dfs in sheet_data.items():
            final_tables[table_name] = pd.concat(dfs, ignore_index=True)

        return final_tables