import os
import logging
from src.db_engine import DBEngine
import psycopg2


def create_tables():
    # Initialize the logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize the DBEngine using the existing class
    db_engine = DBEngine(logger=logger)

    # Path to the SQL file containing the table creation commands
    sql_file_path = os.path.join(os.path.dirname(__file__), 'SMS_tables.sql')

    # Read and execute the SQL script
    try:
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()

        db_engine.cursor.execute(sql_commands)
        db_engine.connection.commit()
        logger.info('Tables created successfully.')

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error creating tables: {error}")
        db_engine.connection.rollback()
        raise


if __name__ == '__main__':
    create_tables()
