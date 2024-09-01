import os
import logging
from src.db_engine import DBEngine
import psycopg2

def create_tables() -> None:
    """Create the necessary tables in the database.

    This function connects to the database using the DBEngine class, reads SQL
    commands from the 'SMS_tables.sql' file, and executes them to create tables.
    If the table creation is successful, a success message is logged. If an
    error occurs, it is logged, the transaction is rolled back, and the error
    is raised.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    db_engine = DBEngine(logger=logger)

    sql_file_path = os.path.join(os.path.dirname(__file__), 'SMS_tables.sql')

    try:
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()

        if db_engine.cursor and db_engine.connection:
            db_engine.cursor.execute(sql_commands)
            db_engine.connection.commit()
            logger.info('Tables created successfully.')
        else:
            raise RuntimeError("Database connection or cursor is not initialized.")

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error creating tables: {error}")
        if db_engine.connection:
            db_engine.connection.rollback()
        raise

if __name__ == '__main__':
    create_tables()
