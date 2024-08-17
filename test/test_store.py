import unittest
from unittest.mock import MagicMock
from src.person.store_table import StoreTable

class TestStoreTable(unittest.TestCase):

    def setUp(self):
        # Create a StoreTable instance and mock DBEngine
        self.store_table = StoreTable()
        self.db_engine_mock = MagicMock()
        self.store_table.db_engine = self.db_engine_mock
        self.db_engine_mock.connection = MagicMock()
        self.db_engine_mock.cursor = MagicMock()

    def test_create_table(self):
        self.store_table.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Store" (
            "StoreID" SERIAL PRIMARY KEY,
            "StoreName" VARCHAR(255) NOT NULL,
            "StoreManagerID" INT NOT NULL,
            "ManagerID" INT NOT NULL,
            "WorkerID" INT NOT NULL,
            "FoodStorageID" INT NOT NULL,
            "DryStoreID" INT NOT NULL
        );
        '''
        self.db_engine_mock.cursor.execute.assert_any_call(create_table_query)

    def test_insert_data(self):
        data = ("SuperMart", 1, 2, 3, 4, 5)
        self.store_table.insert_data(data)
        insert_query = '''
        INSERT INTO "Store" ("StoreName", "StoreManagerID", "ManagerID", "WorkerID", "FoodStorageID", "DryStoreID")
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        self.db_engine_mock.cursor.execute.assert_any_call(insert_query, data)

    def test_update_data(self):
        store_id = 1
        new_values = {
            "StoreName": "SuperMart Updated",
            "StoreManagerID": 10,
            "ManagerID": 20,
            "WorkerID": 30,
            "FoodStorageID": 40,
            "DryStoreID": 50
        }
        self.store_table.update_data(store_id, new_values)
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Store" SET {set_clause} WHERE "StoreID" = %s'
        values = list(new_values.values()) + [store_id]
        self.db_engine_mock.cursor.execute.assert_any_call(update_query, values)

    def test_delete_data(self):
        store_id = 1
        self.store_table.delete_data(store_id)
        delete_query = 'DELETE FROM "Store" WHERE "StoreID" = %s'
        self.db_engine_mock.cursor.execute.assert_any_call(delete_query, (store_id,))

    def test_select_all(self):
        expected_data = [
            (1, "SuperMart", 1, 2, 3, 4, 5),
            (2, "MegaStore", 10, 20, 30, 40, 50)
        ]
        self.db_engine_mock.cursor.fetchall.return_value = expected_data
        result = self.store_table.select_all()
        self.assertEqual(result, expected_data)
        self.db_engine_mock.cursor.execute.assert_any_call('SELECT * FROM "Store"')

    def test_execute_query_failure(self):
        self.db_engine_mock.cursor.execute.side_effect = Exception("Database error")
        with self.assertRaises(Exception):
            query = "SELECT * FROM Store"
            self.store_table._execute_query(query)

    def test_execute_query_success(self):
        query = "SELECT * FROM Store"
        self.store_table._execute_query(query)
        self.db_engine_mock.cursor.execute.assert_any_call(query)

    def test_execute_query_with_params_success(self):
        query = "INSERT INTO Store (name) VALUES (%s)"
        params = ("Test Store",)
        self.store_table._execute_query(query, params)
        self.db_engine_mock.cursor.execute.assert_any_call(query, params)

    def tearDown(self):
        # Clean up the mocks
        self.db_engine_mock.reset_mock()

if __name__ == '__main__':
    unittest.main()
