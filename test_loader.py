from ingestion.excel_reader import ExcelReader
from ingestion.database import PostgreSQL
from ingestion.table_creator import create_raw_table
from ingestion.loader import truncate_raw_table, insert_dataframe_to_raw

reader = ExcelReader()
tables = reader.read_latest_file()

db = PostgreSQL()

for table_name, df in tables.items():
    print("Loading:", table_name)

    create_raw_table(db, df, table_name)
    truncate_raw_table(db, table_name)
    insert_dataframe_to_raw(db, df, table_name)

db.close()

print("✅ Raw data loaded successfully")