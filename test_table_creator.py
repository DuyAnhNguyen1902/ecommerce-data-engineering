from ingestion.excel_reader import ExcelReader
from ingestion.database import PostgreSQL
from ingestion.table_creator import create_raw_table

reader = ExcelReader()
tables = reader.read_latest_file()

db = PostgreSQL()

for table_name, df in tables.items():
    print("Creating table:", table_name)
    create_raw_table(db, df, table_name)

db.close()

print("✅ Raw tables created successfully")