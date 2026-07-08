import psycopg2

from config.settings import *

class PostgreSQL:

    def __init__(self):

        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        self.cursor = self.conn.cursor()

    def execute(self, query):

        self.cursor.execute(query)

        self.conn.commit()

    def close(self):

        self.cursor.close()

        self.conn.close()