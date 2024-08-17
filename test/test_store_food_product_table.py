import unittest
from unittest.mock import MagicMock, patch
from src.person.store_food_product_table import StoreFoodProductTable

class TestStoreFoodProductTable(unittest.TestCase):

    def setUp(self):
        # Create a StoreFoodProductTable instance with a mocked DBEngine
        self.store_food_product_table = StoreFoodProductTable()
        self.store_food_product_table.db_engine = MagicMock()
        self.store_food_product_table.db_engine.connection = MagicMock()
        self.store_food_product_table.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.store_food_product_table._execute_query = MagicMock()
        self.store_food_product_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "StoreFoodProduct" (
            "FoodStorageID" INT NOT NULL,
            "StoreID" INT NOT NULL,
            "FoodID" INT NOT NULL,
            PRIMARY KEY ("FoodStorageID", "StoreID", "FoodID")
        );
        '''
        self.store_food_product_table._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = (1, 2, 3)
        self.store_food_product_table._execute_query = MagicMock()
        self.store_food_product_table.insert_data(data)
        insert_query = '''
        INSERT INTO "StoreFoodProduct" ("FoodStorageID", "StoreID", "FoodID")
        VALUES (%s, %s, %s);
        '''
        self.store_food_product_table._execute_query.assert_called_once_with(insert_query, data)

    def test_delete_data(self):
        food_storage_id, store_id, food_id = 1, 2, 3
        self.store_food_product_table._execute_query = MagicMock()
        self.store_food_product_table.delete_data(food_storage_id, store_id, food_id)
        delete_query = 'DELETE FROM "StoreFoodProduct" WHERE "FoodStorageID" = %s AND "StoreID" = %s AND "FoodID" = %s'
        self.store_food_product_table._execute_query.assert_called_once_with(delete_query, (food_storage_id, store_id, food_id))

    def test_select_all(self):
        self.store_food_product_table.db_engine.cursor.fetchall = MagicMock(return_value=[(1, 2, 3)])
        self.store_food_product_table.select_all()
        self.store_food_product_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "StoreFoodProduct"')

    def test_execute_query_success(self):
        self.store_food_product_table.db_engine.cursor.execute = MagicMock()
        self.store_food_product_table._execute_query('SELECT * FROM "StoreFoodProduct"')
        self.store_food_product_table.db_engine.cursor.execute.assert_called_once_with(
            'SELECT * FROM "StoreFoodProduct"')
        self.store_food_product_table.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.store_food_product_table.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.store_food_product_table._execute_query('SELECT * FROM "StoreFoodProduct"')
            self.store_food_product_table.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')

    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_add_store_food_product(self, mock_input):
        self.store_food_product_table.insert_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_food_product_table.add_store_food_product()
            self.store_food_product_table.insert_data.assert_called_once_with((1, 2, 3))
            mock_print.assert_called_once_with("Store food product added successfully!")

    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_delete_store_food_product(self, mock_input):
        self.store_food_product_table.delete_data = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_food_product_table.delete_store_food_product()
            self.store_food_product_table.delete_data.assert_called_once_with(1, 2, 3)
            mock_print.assert_called_once_with("Store food product deleted successfully!")

    def test_view_store_food_products(self):
        self.store_food_product_table.select_all = MagicMock(return_value=[(1, 2, 3)])
        with patch('builtins.print') as mock_print:
            self.store_food_product_table.view_store_food_products()
            expected_output = "\nStore Food Products:\n(1, 2, 3)"
            mock_print.assert_called_once_with(expected_output)

    @patch('builtins.input', side_effect=['1', '2', '3', '4'])
    def test_manage_store_food_products(self, mock_input):
        self.store_food_product_table.add_store_food_product = MagicMock()
        self.store_food_product_table.delete_store_food_product = MagicMock()
        self.store_food_product_table.view_store_food_products = MagicMock()
        with patch('builtins.print') as mock_print:
            self.store_food_product_table.manage_store_food_products()
            self.store_food_product_table.add_store_food_product.assert_called_once()
            self.store_food_product_table.delete_store_food_product.assert_called_once()
            self.store_food_product_table.view_store_food_products.assert_called_once()

if __name__ == '__main__':
    unittest.main()
