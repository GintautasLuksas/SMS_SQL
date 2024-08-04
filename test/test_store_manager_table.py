import unittest
from unittest.mock import MagicMock, patch
from src.tables.store_manager_table import StoreManagerTable  # Adjust the import path as needed

class TestStoreManagerTable(unittest.TestCase):

    def setUp(self):
        # Create a StoreManagerTable instance with a mocked DBEngine
        self.store_manager_table = StoreManagerTable()
        self.store_manager_table.db_engine = MagicMock()
        self.store_manager_table.db_engine.connection = MagicMock()
        self.store_manager_table.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.store_manager_table._execute_query = MagicMock()
        self.store_manager_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "StoreManager" (
            "StoreManagerID" SERIAL PRIMARY KEY,
            "ManagerID" INT NOT NULL,
            "StoreID" INT NOT NULL
        );
        '''
        self.store_manager_table._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = (1, 2)
        self.store_manager_table._execute_query = MagicMock()
        self.store_manager_table.insert_data(data)
        insert_query = '''
        INSERT INTO "StoreManager" ("ManagerID", "StoreID")
        VALUES (%s, %s);
        '''
        self.store_manager_table._execute_query.assert_called_once_with(insert_query, data)

    def test_update_data(self):
        store_manager_id = 1
        new_values = {'ManagerID': 2, 'StoreID': 3}
        self.store_manager_table._execute_query = MagicMock()
        self.store_manager_table.update_data(store_manager_id, new_values)
        update_query = 'UPDATE "StoreManager" SET "ManagerID" = %s, "StoreID" = %s WHERE "StoreManagerID" = %s'
        values = list(new_values.values()) + [store_manager_id]
        self.store_manager_table._execute_query.assert_called_once_with(update_query, values)

    def test_delete_data(self):
        store_manager_id = 1
        self.store_manager_table._execute_query = MagicMock()
        self.store_manager_table.delete_data(store_manager_id)
        delete_query = 'DELETE FROM "StoreManager" WHERE "StoreManagerID" = %s'
        self.store_manager_table._execute_query.assert_called_once_with(delete_query, (store_manager_id,))

    def test_select_all(self):
        self.store_manager_table.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 2, 3)])
        self.store_manager_table.select_all()
        self.store_manager_table.db_engine.cursor.execute.assert_called_once_with('SELECT * FROM "StoreManager"')

    def test_execute_query_success(self):
        self.store_manager_table.db_engine.cursor.execute = MagicMock()
        self.store_manager_table._execute_query('SELECT * FROM "StoreManager"')
        self.store_manager_table.db_engine.cursor.execute.assert_called_once_with('SELECT * FROM "StoreManager"')
        self.store_manager_table.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.store_manager_table.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.store_manager_table._execute_query('SELECT * FROM "StoreManager"')
            self.store_manager_table.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')

    @patch('builtins.input', side_effect=['1', '2'])
    def test_add_store_manager(self, mock_input):
        self.store_manager_table.insert_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_manager_table.add_store_manager()
            self.store_manager_table.insert_data.assert_called_once_with((1, 2))
            mock_print.assert_called_once_with("Store manager added successfully!")

    @patch('builtins.input', side_effect=['1', '', '3'])
    def test_edit_store_manager(self, mock_input):
        self.store_manager_table.update_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_manager_table.edit_store_manager()
            new_values = {'StoreID': 3}
            self.store_manager_table.update_data.assert_called_once_with(1, new_values)
            mock_print.assert_called_once_with("Store manager updated successfully!")

    @patch('builtins.input', side_effect=['1'])
    def test_delete_store_manager(self, mock_input):
        self.store_manager_table.delete_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_manager_table.delete_store_manager()
            self.store_manager_table.delete_data.assert_called_once_with(1)
            mock_print.assert_called_once_with("Store manager deleted successfully!")

    def test_view_store_managers(self):
        self.store_manager_table.select_all = MagicMock(return_value=[(1, 2, 3)])
        with patch('builtins.print') as mock_print:
            self.store_manager_table.view_store_managers()
            # Check all calls to print
            calls = [patch('builtins.print').call('\nStore Managers:'), patch('builtins.print').call((1, 2, 3))]
            mock_print.assert_has_calls(calls)

    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])
    def test_manage_store_managers(self, mock_input):
        self.store_manager_table.add_store_manager = MagicMock()
        self.store_manager_table.edit_store_manager = MagicMock()
        self.store_manager_table.delete_store_manager = MagicMock()
        self.store_manager_table.view_store_managers = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_manager_table.manage_store_managers()
            self.store_manager_table.add_store_manager.assert_called_once()
            self.store_manager_table.edit_store_manager.assert_called_once()
            self.store_manager_table.delete_store_manager.assert_called_once()
            self.store_manager_table.view_store_managers.assert_called_once()

if __name__ == '__main__':
    unittest.main()
