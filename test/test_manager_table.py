import unittest
from unittest.mock import MagicMock, patch
from src.person.manager_table import ManagerTable

class TestManagerTable(unittest.TestCase):

    def setUp(self):
        # Create a ManagerTable instance with a mocked DBEngine
        self.manager_table = ManagerTable()
        self.manager_table.db_engine = MagicMock()
        self.manager_table.db_engine.connection = MagicMock()
        self.manager_table.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.manager_table._execute_query = MagicMock()
        self.manager_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Manager" (
            "ManagerID" SERIAL PRIMARY KEY,
            "Name" VARCHAR(255) NOT NULL,
            "PhoneNumber" BIGINT NOT NULL,
            "Country" VARCHAR(255) NOT NULL,
            "Email" VARCHAR(255) NOT NULL,
            "MonthlySalary" INT NOT NULL,
            "MGRResponibilityID" INT NOT NULL
        );
        '''
        self.manager_table._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = ("John Doe", 1234567890, "USA", "john.doe@example.com", 5000, 1)
        self.manager_table._execute_query = MagicMock()
        self.manager_table.insert_data(data)
        insert_query = '''
        INSERT INTO "Manager" ("Name", "PhoneNumber", "Country", "Email", "MonthlySalary", "MGRResponibilityID")
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        self.manager_table._execute_query.assert_called_once_with(insert_query, data)

    def test_update_data(self):
        manager_id = 1
        new_values = {
            'Name': 'Jane Doe',
            'PhoneNumber': 9876543210,
            'Country': 'Canada',
            'Email': 'jane.doe@example.com',
            'MonthlySalary': 6000,
            'MGRResponibilityID': 2
        }
        self.manager_table._execute_query = MagicMock()
        self.manager_table.update_data(manager_id, new_values)
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Manager" SET {set_clause} WHERE "ManagerID" = %s'
        values = list(new_values.values()) + [manager_id]
        self.manager_table._execute_query.assert_called_once_with(update_query, values)

    def test_delete_data(self):
        manager_id = 1
        self.manager_table._execute_query = MagicMock()
        self.manager_table.delete_data(manager_id)
        delete_query = 'DELETE FROM "Manager" WHERE "ManagerID" = %s'
        self.manager_table._execute_query.assert_called_once_with(delete_query, (manager_id,))

    def test_select_all(self):
        self.manager_table.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 'John Doe', 1234567890, 'USA', 'john.doe@example.com', 5000, 1)])
        self.manager_table.select_all()
        self.manager_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "Manager"')

    def test_execute_query_success(self):
        self.manager_table.db_engine.cursor.execute = MagicMock()
        self.manager_table._execute_query('SELECT * FROM "Manager"')
        self.manager_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "Manager"')
        self.manager_table.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.manager_table.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.manager_table._execute_query('SELECT * FROM "Manager"')
            self.manager_table.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')

if __name__ == '__main__':
    unittest.main()
