import unittest
from unittest.mock import MagicMock, patch
from src.tables.manager_responsibilities_table import ManagerResponsibilitiesTable


class TestManagerResponsibilitiesTable(unittest.TestCase):

    def setUp(self):
        # Create a ManagerResponsibilitiesTable instance with a mocked DBEngine
        self.manager_responsibilities = ManagerResponsibilitiesTable()
        self.manager_responsibilities.db_engine = MagicMock()
        self.manager_responsibilities.db_engine.connection = MagicMock()
        self.manager_responsibilities.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.manager_responsibilities._execute_query = MagicMock()
        self.manager_responsibilities.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Manager Responsibilities" (
            "MGRResponsibilityID" INT NOT NULL,
            "ResponsibilityID" INT NOT NULL,
            "ManagerID" INT NOT NULL,
            PRIMARY KEY ("MGRResponsibilityID")
        );
        '''
        self.manager_responsibilities._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = (1, 2, 3)
        self.manager_responsibilities._execute_query = MagicMock()
        self.manager_responsibilities.insert_data(data)
        insert_query = '''
        INSERT INTO "Manager Responsibilities" ("MGRResponsibilityID", "ResponsibilityID", "ManagerID")
        VALUES (%s, %s, %s);
        '''
        self.manager_responsibilities._execute_query.assert_called_once_with(insert_query, data)

    def test_delete_data(self):
        mgr_responsibility_id = 1
        self.manager_responsibilities._execute_query = MagicMock()
        self.manager_responsibilities.delete_data(mgr_responsibility_id)
        delete_query = 'DELETE FROM "Manager Responsibilities" WHERE "MGRResponsibilityID" = %s'
        self.manager_responsibilities._execute_query.assert_called_once_with(delete_query, (mgr_responsibility_id,))

    def test_select_all(self):
        self.manager_responsibilities.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 2, 3)])
        self.manager_responsibilities.select_all()
        self.manager_responsibilities.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "Manager Responsibilities"')

    def test_execute_query_success(self):
        self.manager_responsibilities.db_engine.cursor.execute = MagicMock()
        self.manager_responsibilities._execute_query('SELECT * FROM "Manager Responsibilities"')
        self.manager_responsibilities.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "Manager Responsibilities"')
        self.manager_responsibilities.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.manager_responsibilities.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.manager_responsibilities._execute_query('SELECT * FROM "Manager Responsibilities"')
            self.manager_responsibilities.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')


if __name__ == '__main__':
    unittest.main()
