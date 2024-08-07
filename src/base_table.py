import psycopg2

from db_engine import DBEngine
from psycopg2 import sql
import logging

logger = logging.getLogger(__name__)


class BaseTable:
    def __init__(self, table_name, columns):
        '''

        :param table_name:
        :param columns:
        '''
        self.table_name = table_name
        self.columns = columns
        self.db_connection = DBEngine()
        self.create_table()

    def create_table(self):

        column_definitions = ', '.join(
            f'"{col}" {dtype}' for col, dtype in self.columns.items()
        )
        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table} (
                {columns}
            )
        """).format(
            table=sql.Identifier(self.table_name),
            columns=sql.SQL(column_definitions)
        )
        try:
            logger.info(f'Creating table {self.table_name}...')
            self.db_connection.cursor.execute(query)
            self.db_connection.connection.commit()
            logger.info(f'Table {self.table_name} created or already exists!')
        except psycopg2.Error as e:
            logger.error(f"Error creating table {self.table_name}: {e}")
            self.db_connection.connection.rollback()

    def insert_data(self, df):

        columns = sql.SQL(', ').join(map(sql.Identifier, self.columns.keys()))
        values = sql.SQL(', ').join(sql.Placeholder() * len(self.columns))
        query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values}) ON CONFLICT DO NOTHING").format(
            table=sql.Identifier(self.table_name),
            fields=columns,
            values=values
        )
        data = [tuple(row) for row in df.to_numpy()]
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.executemany(query, data)
                self.db_connection.connection.commit()
            logger.info(f'Data inserted into {self.table_name} successfully!')
        except psycopg2.Error as e:
            logger.error(f"Error inserting data into {self.table_name}: {e}")
            self.db_connection.connection.rollback()

    def update_data(self, identifier_col, identifier_value, new_values):

        set_clause = sql.SQL(', ').join(
            sql.SQL("{field} = %s").format(field=sql.Identifier(k)) for k in new_values.keys()
        )
        query = sql.SQL("UPDATE {table} SET {set_clause} WHERE {identifier_col} = %s").format(
            table=sql.Identifier(self.table_name),
            set_clause=set_clause,
            identifier_col=sql.Identifier(identifier_col)
        )
        try:
            self.db_connection.cursor.execute(query, (*new_values.values(), identifier_value))
            self.db_connection.connection.commit()
            logger.info(f'Data in {self.table_name} updated successfully!')
        except psycopg2.Error as e:
            logger.error(f"Error updating data in {self.table_name}: {e}")
            self.db_connection.connection.rollback()

    def delete_data(self, identifier_col, identifier_value):

        query = sql.SQL("DELETE FROM {table} WHERE {identifier_col} = %s").format(
            table=sql.Identifier(self.table_name),
            identifier_col=sql.Identifier(identifier_col)
        )
        try:
            self.db_connection.cursor.execute(query, (identifier_value,))
            self.db_connection.connection.commit()
            logger.info(f'Data from {self.table_name} deleted successfully!')
        except psycopg2.Error as e:
            logger.error(f"Error deleting data from {self.table_name}: {e}")
            self.db_connection.connection.rollback()

    def select_all(self):

        query = sql.SQL("SELECT DISTINCT * FROM {table}").format(table=sql.Identifier(self.table_name))
        try:
            self.db_connection.cursor.execute(query)
            return self.db_connection.cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Error retrieving data from {self.table_name}: {e}")
            return []

    def drop_table(self):

        query = sql.SQL("DROP TABLE IF EXISTS {table}").format(table=sql.Identifier(self.table_name))
        try:
            self.db_connection.cursor.execute(query)
            self.db_connection.connection.commit()
            logger.info(f'Table {self.table_name} dropped successfully!')
        except psycopg2.Error as e:
            logger.error(f"Error dropping table {self.table_name}: {e}")
            self.db_connection.connection.rollback()
