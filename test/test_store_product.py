import unittest
from unittest.mock import patch, MagicMock
from src.store.store_product import StoreDryProduct, StoreFoodProduct

def normalize_query(query: str) -> str:
    """Helper function to normalize SQL queries by removing all excess whitespace."""
    return ' '.join(query.split())

class TestStoreDryProduct(unittest.TestCase):
    """Test suite for the `StoreDryProduct` class."""

    @patch('src.store.store_product.DBEngine')
    def test_add_dry_storage_item_to_store(self, mock_db_engine: MagicMock) -> None:
        """Test adding a dry storage item to a store."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreDryProduct.add(store_id=1, dry_storage_id=2)

        expected_query = """
            INSERT INTO "StoreDryProduct" ("StoreID", "DryStorageID")
            VALUES (%s, %s)
        """
        # Normalize the actual and expected queries before comparison
        actual_query, actual_params = mock_cursor.execute.call_args[0]
        self.assertEqual(normalize_query(expected_query), normalize_query(actual_query))
        self.assertEqual(actual_params, (1, 2))

    @patch('src.store.store_product.DBEngine')
    def test_remove_dry_storage_item_from_store(self, mock_db_engine: MagicMock) -> None:
        """Test removing a dry storage item from a store."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreDryProduct.remove(store_id=1, dry_storage_id=2)

        expected_query = """
            DELETE FROM "StoreDryProduct"
            WHERE "StoreID" = %s AND "DryStorageID" = %s
        """
        # Normalize the actual and expected queries before comparison
        actual_query, actual_params = mock_cursor.execute.call_args[0]
        self.assertEqual(normalize_query(expected_query), normalize_query(actual_query))
        self.assertEqual(actual_params, (1, 2))

class TestStoreFoodProduct(unittest.TestCase):
    """Test suite for the `StoreFoodProduct` class."""

    @patch('src.store.store_product.DBEngine')
    def test_add_food_item_to_store(self, mock_db_engine: MagicMock) -> None:
        """Test adding a food item to a store."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreFoodProduct.add(store_id=1, food_id=2)

        expected_query = """
            INSERT INTO "StoreFoodProduct" ("StoreID", "FoodID")
            VALUES (%s, %s)
        """
        # Normalize the actual and expected queries before comparison
        actual_query, actual_params = mock_cursor.execute.call_args[0]
        self.assertEqual(normalize_query(expected_query), normalize_query(actual_query))
        self.assertEqual(actual_params, (1, 2))

    @patch('src.store.store_product.DBEngine')
    def test_remove_food_item_from_store(self, mock_db_engine: MagicMock) -> None:
        """Test removing a food item from a store."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreFoodProduct.remove(store_id=1, food_id=2)

        expected_query = """
            DELETE FROM "StoreFoodProduct"
            WHERE "StoreID" = %s AND "FoodID" = %s
        """
        # Normalize the actual and expected queries before comparison
        actual_query, actual_params = mock_cursor.execute.call_args[0]
        self.assertEqual(normalize_query(expected_query), normalize_query(actual_query))
        self.assertEqual(actual_params, (1, 2))

if __name__ == '__main__':
    unittest.main()
