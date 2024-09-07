import unittest
from unittest.mock import patch, MagicMock
from src.store.store import Store


class TestStore(unittest.TestCase):

    def normalize_sql(self, sql: str) -> str:
        """Utility function to normalize SQL by removing extra spaces and newlines."""
        return ' '.join(sql.split())

    @patch('src.store.store.DBEngine')
    def test_create_new_store(self, mock_db_engine: MagicMock) -> None:
        """Test creating a new store and assigning an ID."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Simulate returning new store ID
        mock_db_engine.return_value.__enter__.return_value.cursor = mock_cursor

        store = Store(store_name="Test Store")
        store.save()

        self.assertEqual(store.store_id, 1)

        # Ensure the query was executed with expected parameters
        mock_cursor.execute.assert_called_once()
        query = mock_cursor.execute.call_args[0][0]  # SQL query
        params = mock_cursor.execute.call_args[0][1]  # SQL parameters
        self.assertIn("INSERT INTO", self.normalize_sql(query))
        self.assertIn("StoreName", self.normalize_sql(query))
        self.assertEqual(params, ('Test Store',))

    @patch('src.store.store.DBEngine')
    def test_update_existing_store(self, mock_db_engine: MagicMock) -> None:
        """Test updating an existing store."""
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value.cursor = mock_cursor

        store = Store(store_name="Updated Store", store_id=1)
        store.save()

        # Ensure the query was executed with expected parameters
        mock_cursor.execute.assert_called_once()
        query = mock_cursor.execute.call_args[0][0]  # SQL query
        params = mock_cursor.execute.call_args[0][1]  # SQL parameters
        self.assertIn("UPDATE", self.normalize_sql(query))
        self.assertIn("StoreName", self.normalize_sql(query))
        self.assertIn("WHERE", self.normalize_sql(query))
        self.assertEqual(params, ('Updated Store', 1))

    @patch('src.store.store.DBEngine')
    def test_delete_store(self, mock_db_engine: MagicMock) -> None:
        """Test deleting a store from the database."""
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value.cursor = mock_cursor

        store = Store(store_name="Test Store", store_id=1)
        store.delete()

        self.assertIsNone(store.store_id)

        # Ensure the delete query was executed
        mock_cursor.execute.assert_called_once()
        query = mock_cursor.execute.call_args[0][0]  # SQL query
        params = mock_cursor.execute.call_args[0][1]  # SQL parameters
        self.assertIn("DELETE FROM", self.normalize_sql(query))
        self.assertIn("StoreID", self.normalize_sql(query))
        self.assertEqual(params, (1,))

    @patch('src.store.store.DBEngine')
    def test_view_all_stores(self, mock_db_engine: MagicMock) -> None:
        """Test retrieving all stores from the database."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Store A"),
            (2, "Store B")
        ]
        mock_db_engine.return_value.__enter__.return_value.cursor = mock_cursor

        stores = Store.view_all()

        # Ensure stores is not None before further assertions
        self.assertIsNotNone(stores, "Expected a list of stores, but got None")

        if stores is not None:
            self.assertEqual(len(stores), 2)
            self.assertEqual(stores[0], (1, "Store A"))
            self.assertEqual(stores[1], (2, "Store B"))

        # Ensure the query was executed correctly
        mock_cursor.execute.assert_called_once()
        query = mock_cursor.execute.call_args[0][0]  # SQL query
        self.assertIn('SELECT', self.normalize_sql(query))
        self.assertIn('"StoreID"', self.normalize_sql(query))
        self.assertIn('"StoreName"', self.normalize_sql(query))


if __name__ == '__main__':
    unittest.main()
