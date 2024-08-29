import os
import psycopg2
from psycopg2.extensions import connection as Psycopg2Connection, cursor as Psycopg2Cursor
from dotenv import load_dotenv
import logging
from typing import Optional, Type, Any

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

class DBEngine:
    """
    DBEngine is responsible for managing the connection to the PostgreSQL database.

    This class handles establishing and closing connections, as well as managing
    the database cursor. It utilizes environment variables for connection parameters.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initializes the DBEngine instance and establishes a database connection.

        :param logger: Optional logging.Logger instance. If not provided, a default logger is used.
        """
        self.connection: Optional[Psycopg2Connection] = None
        self.cursor: Optional[Psycopg2Cursor] = None
        self.logger: logging.Logger = logger or logging.getLogger(__name__)
        self.connect()

    def connect(self) -> None:
        """
        Establishes a connection to the PostgreSQL database using credentials from environment variables.

        Logs the success or failure of the connection attempt.
        """
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

    def __enter__(self) -> 'DBEngine':
        """
        Enter the runtime context related to this object.

        :return: The DBEngine instance.
        """
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """
        Exit the runtime context related to this object, closing the connection and cursor.

        :param exc_type: The exception type.
        :param exc_val: The exception value.
        :param exc_tb: The traceback object.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info('Database connection closed.')
