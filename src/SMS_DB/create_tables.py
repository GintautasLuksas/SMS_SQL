import os
import logging
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from src.db_engine import DBEngine

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)


def database_exists(conn, dbname):
    """Check if the specified database exists."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        return cursor.fetchone() is not None


def table_exists(db_engine, table_name):
    """Check if the specified table exists in the database."""
    query = sql.SQL("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
        );
    """)
    db_engine.cursor.execute(query, (table_name,))
    return db_engine.cursor.fetchone()[0]


def create_database_if_not_exists():
    """Create the database if it does not exist."""
    server_conn_params = {
        'dbname': 'postgres',
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT'),
    }

    conn = None
    try:
        conn = psycopg2.connect(**server_conn_params)
        conn.autocommit = True
        with conn.cursor() as cursor:
            if not database_exists(conn, 'SMS'):
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('SMS')))
                logging.info("Database 'SMS' created successfully.")
            else:
                logging.info("Database 'SMS' already exists.")
    except psycopg2.Error as error:
        logging.error(f"Error checking/creating database: {error}")
        raise
    finally:
        if conn is not None:
            conn.close()


def execute_sql_commands_from_file(db_engine, file_path):
    """Execute SQL commands from a file."""
    try:
        with open(file_path, 'r') as file:
            sql_commands = file.read()

        # Split the SQL file into individual commands
        commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]

        for command in commands:
            if command.strip():  # Skip empty commands
                try:
                    # Check if the table exists before attempting to create it
                    if "CREATE TABLE" in command.upper():
                        # Extract table name from the SQL command
                        start_idx = command.upper().find("CREATE TABLE") + len("CREATE TABLE")
                        end_idx = command.upper().find("(", start_idx)
                        table_name = command[start_idx:end_idx].strip().strip('"').strip("'")

                        if table_exists(db_engine, table_name):
                            logging.info(f"Table '{table_name}' already exists. Skipping creation.")
                            continue

                    # Execute SQL command
                    db_engine.cursor.execute(command)
                    logging.info(f"Successfully executed command: {command}")
                except psycopg2.Error as error:
                    logging.error(f"Error executing command: {command}\n{error}")
                    db_engine.connection.rollback()
    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error executing SQL commands: {error}")
        db_engine.connection.rollback()
        raise


def create_tables():
    """Create the database and tables."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    create_database_if_not_exists()

    db_engine = DBEngine(logger=logger)

    try:
        sql_file_path = os.path.join(os.path.dirname(__file__), 'SMS_tables.sql')
        execute_sql_commands_from_file(db_engine, sql_file_path)
    finally:
        db_engine.connection.close()
        del db_engine


if __name__ == '__main__':
    create_tables()
