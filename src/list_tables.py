import os
from dotenv import load_dotenv
import psycopg2
from src.db_engine import DBEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the .env file from the config directory
dotenv_path = os.path.join(os.path.dirname(__file__), '../config/.env')
load_dotenv(dotenv_path)

def list_tables():
    db_engine = DBEngine()
    cursor = db_engine.cursor

    try:
        if cursor:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """
            cursor.execute(query)
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error retrieving tables: {error}")
    finally:
        if cursor:
            cursor.close()
        if db_engine.connection:
            db_engine.connection.close()

if __name__ == "__main__":
    list_tables()
