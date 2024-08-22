import os
import logging
import psycopg2

from db_engine import DBEngine


def create_tables():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    db_engine = DBEngine(logger=logger)


    sql_file_path = os.path.join(os.path.dirname(__file__), 'SMS_tables.sql')

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
