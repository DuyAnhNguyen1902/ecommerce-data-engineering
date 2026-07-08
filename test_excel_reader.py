from ingestion.excel_reader import ExcelReader

reader = ExcelReader()
tables = reader.read_latest_file()

for table_name, df in tables.items():
    print(table_name, df.shape)
    print(df.head())