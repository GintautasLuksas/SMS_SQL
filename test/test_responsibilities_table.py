import unittest
from unittest.mock import MagicMock, patch
from src.tables.responsibilities_table import ResponsibilitiesTable

class TestResponsibilitiesTable(unittest.TestCase):

    def setUp(self):
        # Create a ResponsibilitiesTable instance with a mocked DBEngine
        self.responsibilities_table = ResponsibilitiesTable()
        self.responsibilities_table.db_engine = MagicMock()
        self.responsibilities_table.db_engine.connection = MagicMock()
        self.responsibilities_table.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.responsibilities_table._execute_query = MagicMock()
        self.responsibilities_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Responsibilities" (
            "ResponsibilityID" SERIAL PRIMARY KEY,
            "ResponsibilityName" VARCHAR(255) NOT NULL
        );
        '''
        self.responsibilities_table._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = ("Manage team",)
        self.responsibilities_table._execute_query = MagicMock()
        self.responsibilities_table.insert_data(data)
        insert_query = '''
        INSERT INTO "Responsibilities" ("ResponsibilityName")
        VALUES (%s);
        '''
        self.responsibilities_table._execute_query.assert_called_once_with(insert_query, data)

    def test_update_data(self):
        responsibility_id = 1
        new_values = {
            'ResponsibilityName': 'Lead team'
        }
        self.responsibilities_table._execute_query = MagicMock()
        self.responsibilities_table.update_data(responsibility_id, new_values)
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Responsibilities" SET {set_clause} WHERE "ResponsibilityID" = %s'
        values = list(new_values.values()) + [responsibility_id]
        self.responsibilities_table._execute_query.assert_called_once_with(update_query, values)

    def test_delete_data(self):
        responsibility_id = 1
        self.responsibilities_table._execute_query = MagicMock()
        self.responsibilities_table.delete_data(responsibility_id)
        delete_query = 'DELETE FROM "Responsibilities" WHERE "ResponsibilityID" = %s'
        self.responsibilities_table._execute_query.assert_called_once_with(delete_query, (responsibility_id,))

    def test_select_all(self):
        self.responsibilities_table.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 'Manage team')])
        self.responsibilities_table.select_all()
        self.responsibilities_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "Responsibilities"')

    def test_execute_query_success(self):
        self.responsibilities_table.db_engine.cursor.execute = MagicMock()
        self.responsibilities_table._execute_query('SELECT * FROM "Responsibilities"')
        self.responsibilities_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "Responsibilities"')
        self.responsibilities_table.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.responsibilities_table.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.responsibilities_table._execute_query('SELECT * FROM "Responsibilities"')
            self.responsibilities_table.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')

if __name__ == '__main__':
    unittest.main()
