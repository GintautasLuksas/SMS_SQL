import os
import psycopg2
from dotenv import load_dotenv
import logging

# Specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Debugging: Print environment variables to ensure they are loaded
print("DB Name:", os.getenv('DB_NAME'))
print("DB User:", os.getenv('DB_USERNAME'))
print("DB Password:", os.getenv('DB_PASSWORD'))
print("DB Host:", os.getenv('HOST'))
print("DB Port:", os.getenv('PORT'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBEngine:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USERNAME'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('HOST'),
                port=os.getenv('PORT')
            )
            self.cursor = self.connection.cursor()
            logger.info('Database connection established.')
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Error connecting to the database: {error}")
            raise

    def __del__(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info('Database connection closed.')
