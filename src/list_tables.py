import os
from dotenv import load_dotenv  # type: ignore
import psycopg2  # type: ignore
from src.db_engine import DBEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), '../config/.env')
load_dotenv(dotenv_path=dotenv_path)

def list_tables() -> None:
    """
    Retrieves and prints the names of all tables in the public schema of the PostgreSQL database.

    This function connects to the database using the DBEngine class, executes a query to retrieve
    the list of table names, and then prints each table name. If an error occurs during the process,
    it logs the error message.

    The database connection and cursor are closed after the operation.
    """
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
