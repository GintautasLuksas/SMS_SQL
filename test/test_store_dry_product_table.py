import unittest
from unittest.mock import MagicMock, patch
from src.tables.store_dry_product_table import StoreDryProductTable

class TestStoreDryProductTable(unittest.TestCase):

    def setUp(self):
        # Create a StoreDryProductTable instance with a mocked DBEngine
        self.store_dry_product_table = StoreDryProductTable()
        self.store_dry_product_table.db_engine = MagicMock()
        self.store_dry_product_table.db_engine.connection = MagicMock()
        self.store_dry_product_table.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.store_dry_product_table._execute_query = MagicMock()
        self.store_dry_product_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "StoreDryProduct" (
            "DryStoreID" INT NOT NULL,
            "StoreID" INT NOT NULL,
            "DryStorageID" INT NOT NULL,
            PRIMARY KEY ("DryStoreID", "StoreID", "DryStorageID")
        );
        '''
        self.store_dry_product_table._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = (1, 2, 3)
        self.store_dry_product_table._execute_query = MagicMock()
        self.store_dry_product_table.insert_data(data)
        insert_query = '''
        INSERT INTO "StoreDryProduct" ("DryStoreID", "StoreID", "DryStorageID")
        VALUES (%s, %s, %s);
        '''
        self.store_dry_product_table._execute_query.assert_called_once_with(insert_query, data)

    def test_delete_data(self):
        dry_store_id, store_id, dry_storage_id = 1, 2, 3
        self.store_dry_product_table._execute_query = MagicMock()
        self.store_dry_product_table.delete_data(dry_store_id, store_id, dry_storage_id)
        delete_query = 'DELETE FROM "StoreDryProduct" WHERE "DryStoreID" = %s AND "StoreID" = %s AND "DryStorageID" = %s'
        self.store_dry_product_table._execute_query.assert_called_once_with(delete_query, (dry_store_id, store_id, dry_storage_id))

    def test_select_all(self):
        self.store_dry_product_table.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 2, 3)])
        self.store_dry_product_table.select_all()
        self.store_dry_product_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "StoreDryProduct"')

    def test_execute_query_success(self):
        self.store_dry_product_table.db_engine.cursor.execute = MagicMock()
        self.store_dry_product_table._execute_query('SELECT * FROM "StoreDryProduct"')
        self.store_dry_product_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "StoreDryProduct"')
        self.store_dry_product_table.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.store_dry_product_table.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.store_dry_product_table._execute_query('SELECT * FROM "StoreDryProduct"')
            self.store_dry_product_table.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')

    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_add_store_dry_product(self, mock_input):
        self.store_dry_product_table.insert_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_dry_product_table.add_store_dry_product()
            self.store_dry_product_table.insert_data.assert_called_once_with((1, 2, 3))
            mock_print.assert_called_once_with("Store dry product added successfully!")

    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_delete_store_dry_product(self, mock_input):
        self.store_dry_product_table.delete_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_dry_product_table.delete_store_dry_product()
            self.store_dry_product_table.delete_data.assert_called_once_with(1, 2, 3)
            mock_print.assert_called_once_with("Store dry product deleted successfully!")

    def test_view_store_dry_products(self):
        self.store_dry_product_table.select_all = MagicMock(return_value=[(1, 2, 3)])
        with patch('builtins.print') as mock_print:
            self.store_dry_product_table.view_store_dry_products()
            mock_print.assert_called_once_with("\nStore Dry Products:\n(1, 2, 3)")

    @patch('builtins.input', side_effect=['1', '2', '3', '4'])
    def test_manage_store_dry_products(self, mock_input):
        self.store_dry_product_table.add_store_dry_product = MagicMock()
        self.store_dry_product_table.delete_store_dry_product = MagicMock()
        self.store_dry_product_table.view_store_dry_products = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_dry_product_table.manage_store_dry_products()
            self.store_dry_product_table.add_store_dry_product.assert_called_once()
            self.store_dry_product_table.delete_store_dry_product.assert_called_once()
            self.store_dry_product_table.view_store_dry_products.assert_called_once()

if __name__ == '__main__':
    unittest.main()
