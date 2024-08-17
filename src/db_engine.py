import os
import psycopg2
from dotenv import load_dotenv
import logging

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

class DBEngine:
    def __init__(self, logger=None):
        self.connection = None
        self.cursor = None
        self.logger = logger or logging.getLogger(__name__)
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('HOST'),
                port=os.getenv('PORT')
            )
            self.cursor = self.connection.cursor()
            self.logger.info('Database connection established.')
        except (Exception, psycopg2.Error) as error:
            self.logger.error(f"Error connecting to the database: {error}")
            raise

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info('Database connection closed.')
