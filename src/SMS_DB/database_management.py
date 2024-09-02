import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv, set_key
import logging
from src.db_engine import DBEngine
from typing import Optional

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
config_directory = os.path.dirname(dotenv_path)
if not os.path.exists(config_directory):
    os.makedirs(config_directory)

load_dotenv(dotenv_path=dotenv_path)


def create_or_update_env_file(db_name: str = 'SMS', db_user: str = '', db_password: str = '', host: str = '',
                              port: str = '') -> None:
    """Create or update the .env file with the provided database connection details.

    Directly updates the .env file with the provided values.

    :param db_name: Name of the database, default is 'SMS'.
    :param db_user: Username for the database connection.
    :param db_password: Password for the database connection.
    :param host: Host address of the PostgreSQL server.
    :param port: Port number of the PostgreSQL server.
    """
    # Set each key in the .env file with the provided value
    set_key(dotenv_path, 'DB_NAME', db_name)
    set_key(dotenv_path, 'DB_USERNAME', db_user)
    set_key(dotenv_path, 'DB_PASSWORD', db_password)
    set_key(dotenv_path, 'HOST', host)
    set_key(dotenv_path, 'PORT', port)

    print(".env file updated with new database connection details.")


def create_database_if_not_exists(logger: logging.Logger) -> None:
    """Check if the 'SMS' database exists and create it if it does not.

    Establishes a connection to the default 'postgres' database and checks for
    the existence of the 'SMS' database. Creates the database if it does not exist.

    :param logger: A logging.Logger instance for logging database creation activities.
    """
    db_name = os.getenv('DB_NAME', 'SMS')  # Default to 'SMS' if DB_NAME not set in .env
    db_user = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            logger.info(f"Database '{db_name}' created successfully.")
        else:
            logger.info(f"Database '{db_name}' already exists.")

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error while checking/creating the database: {error}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def create_tables() -> None:
    """Create the necessary tables in the 'SMS' database using SQL commands from 'SMS_tables.sql'.

    Connects to the 'SMS' database using the DBEngine class, reads SQL commands from the
    'SMS_tables.sql' file, and executes them to create tables. Logs the success or failure of
    the table creation and continues gracefully if a table already exists.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    create_database_if_not_exists(logger)

    db_engine = DBEngine(logger=logger)
    sql_file_path = os.path.join(os.path.dirname(__file__), 'SMS_tables.sql')

    try:
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()

        if db_engine.cursor and db_engine.connection:
            try:
                db_engine.cursor.execute(sql_commands)
                db_engine.connection.commit()
                logger.info('Tables created successfully.')
            except psycopg2.errors.DuplicateTable as e:
                logger.warning(f"Some tables already exist. Continuing without error: {e}")
                db_engine.connection.commit()
            except Exception as e:
                logger.error(f"Error executing SQL commands: {e}")
                db_engine.connection.rollback()
                raise
        else:
            raise RuntimeError("Database connection or cursor is not initialized.")

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error creating tables: {error}")
    finally:
        db_engine.__exit__(None, None, None)


def list_tables() -> None:
    """List all tables in the 'SMS' database.

    Connects to the 'SMS' database using the DBEngine class and retrieves the names
    of all tables in the public schema. Prints each table name to the console.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    db_engine = DBEngine(logger=logger)

    try:
        if db_engine.cursor:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """
            db_engine.cursor.execute(query)
            tables = db_engine.cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        else:
            logger.error("Database connection or cursor is not initialized.")

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error retrieving tables: {error}")
    finally:
        if db_engine.cursor:
            db_engine.cursor.close()
        if db_engine.connection:
            db_engine.connection.close()


def database_management_menu() -> None:
    """Display a menu for database management options.

    Provides options to create or update the .env file, check or create the database,
    create tables, list tables, and exit. Handles user input to perform these actions.
    """
    while True:
        print("\nDatabase Management Menu")
        print("1. Create or Update .env File")
        print("2. Check/Create Database and Create Tables")
        print("3. List Tables in Database")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # Allow the user to enter new values for the .env file
            db_user = input("Enter DB_USERNAME (default: 'postgres'): ") or 'postgres'
            db_password = input("Enter DB_PASSWORD): ") or 'Latvia1'
            host = input("Enter HOST (default: 'localhost'): ") or 'localhost'
            port = input("Enter PORT (default: '5432'): ") or '5432'
            create_or_update_env_file(db_user=db_user, db_password=db_password, host=host, port=port)
        elif choice == '2':
            create_tables()
        elif choice == '3':
            list_tables()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please select between 1 and 4.")


if __name__ == '__main__':
    database_management_menu()
