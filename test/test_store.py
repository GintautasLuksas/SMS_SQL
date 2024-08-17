import unittest
from unittest.mock import patch, MagicMock
from src.db_engine import DBEngine
from src.store.store import Store

class TestStore(unittest.TestCase):

    @patch('your_module.DBEngine')
    def test_store_create(self, MockDBEngine):
        # Test creating a new store
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchone.return_value = [1]

        store = Store(store_name="Test Store")

        store.save()

        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO "Store" ("StoreName")
            VALUES (%s)
            RETURNING "StoreID"
            """,
            ("Test Store",)
        )
        self.assertEqual(store.store_id, 1)

    @patch('your_module.DBEngine')  # Mock DBEngine in the module where Store is defined
    def test_store_update(self, MockDBEngine):
        # Test updating an existing store
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        store = Store(store_name="Test Store", store_id=1)

        store.save()

        mock_cursor.execute.assert_called_once_with(
            """
            UPDATE "Store"
            SET "StoreName" = %s
            WHERE "StoreID" = %s
            """,
            ("Test Store", 1)
        )

    @patch('your_module.DBEngine')  # Mock DBEngine in the module where Store is defined
    def test_store_delete(self, MockDBEngine):
        # Test deleting a store
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        store = Store(store_name="Test Store", store_id=1)

        store.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Store" WHERE "StoreID" = %s',
            (1,)
        )
        self.assertIsNone(store.store_id)

    @patch('your_module.DBEngine')  # Mock DBEngine in the module where Store is defined
    def test_view_all_stores(self, MockDBEngine):
        # Test viewing all stores
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchall.return_value = [(1, "Test Store")]

        stores = Store.view_all()

        mock_cursor.execute.assert_called_once_with('SELECT "StoreID", "StoreName" FROM "Store"')
        self.assertEqual(len(stores), 1)
        self.assertEqual(stores[0], (1, "Test Store"))

if __name__ == '__main__':
    unittest.main()
