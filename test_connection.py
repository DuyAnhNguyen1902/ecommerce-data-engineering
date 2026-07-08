from ingestion.database import PostgreSQL

db = PostgreSQL()

print("✅ Connected to PostgreSQL!")

db.close()