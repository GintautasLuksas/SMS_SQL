import unittest
from unittest.mock import MagicMock, patch
from src.person.sm_responsibilities_table import SMResponsibilitiesTable

class TestSMResponsibilitiesTable(unittest.TestCase):

    def setUp(self):
        # Create an SMResponsibilitiesTable instance with a mocked DBEngine
        self.sm_responsibilities_table = SMResponsibilitiesTable()
        self.sm_responsibilities_table.db_engine = MagicMock()
        self.sm_responsibilities_table.db_engine.connection = MagicMock()
        self.sm_responsibilities_table.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.sm_responsibilities_table._execute_query = MagicMock()
        self.sm_responsibilities_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "SM Responsibilities" (
            "SMResponsibilityID" INT NOT NULL,
            "ResponsibilityID" INT NOT NULL,
            "StoreManagerID" INT NOT NULL,
            PRIMARY KEY ("SMResponsibilityID")
        );
        '''
        self.sm_responsibilities_table._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = (1, 2, 3)
        self.sm_responsibilities_table._execute_query = MagicMock()
        self.sm_responsibilities_table.insert_data(data)
        insert_query = '''
        INSERT INTO "SM Responsibilities" ("SMResponsibilityID", "ResponsibilityID", "StoreManagerID")
        VALUES (%s, %s, %s);
        '''
        self.sm_responsibilities_table._execute_query.assert_called_once_with(insert_query, data)

    def test_delete_data(self):
        sm_responsibility_id = 1
        self.sm_responsibilities_table._execute_query = MagicMock()
        self.sm_responsibilities_table.delete_data(sm_responsibility_id)
        delete_query = 'DELETE FROM "SM Responsibilities" WHERE "SMResponsibilityID" = %s'
        self.sm_responsibilities_table._execute_query.assert_called_once_with(delete_query, (sm_responsibility_id,))

    def test_select_all(self):
        self.sm_responsibilities_table.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 2, 3)])
        self.sm_responsibilities_table.select_all()
        self.sm_responsibilities_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "SM Responsibilities"')

    def test_execute_query_success(self):
        self.sm_responsibilities_table.db_engine.cursor.execute = MagicMock()
        self.sm_responsibilities_table._execute_query('SELECT * FROM "SM Responsibilities"')
        self.sm_responsibilities_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "SM Responsibilities"')
        self.sm_responsibilities_table.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.sm_responsibilities_table.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.sm_responsibilities_table._execute_query('SELECT * FROM "SM Responsibilities"')
            self.sm_responsibilities_table.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')

if __name__ == '__main__':
    unittest.main()
