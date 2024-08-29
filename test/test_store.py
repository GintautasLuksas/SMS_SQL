"""
Unit tests for the `Store` class in the `store.py` module.

This script tests the functionality of CRUD operations on the `Store` class,
ensuring correct interactions with the database.

Pre-commit best practices:
- Ensure imports are sorted and used properly.
- Include clear, concise docstrings for each test case.
- Avoid long lines and enforce PEP8 compliance.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.store.store import Store
from src.db_engine import DBEngine


class TestStore(unittest.TestCase):
    """
    Test suite for the `Store` class.
    """

    @patch('src.store.store.DBEngine')
    def test_create_new_store(self, mock_db_engine):
        """
        Test that a new store is correctly created and assigned an ID.

        Verifies that a new store is saved to the database, and checks if a new ID is returned.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Simulate returning new ID
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        store = Store(store_name="Test Store")
        store.save()

        self.assertEqual(store.store_id, 1)
        mock_cursor.execute.assert_called_once()

    @patch('src.store.store.DBEngine')
    def test_delete_store(self, mock_db_engine):
        """
        Test that a store is correctly deleted from the database.

        Verifies that an existing store is deleted from the database and checks if the ID is set to None.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        store = Store(store_name="Test Store", store_id=1)
        store.delete()

        self.assertIsNone(store.store_id)
        mock_cursor.execute.assert_called_once_with('DELETE FROM "Store" WHERE "StoreID" = %s', (1,))

    @patch('src.store.store.DBEngine')
    def test_view_all_stores(self, mock_db_engine):
        """
        Test that all stores are correctly retrieved from the database.

        Simulates retrieval of multiple stores from the database and checks the output list for correct entries.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Store A"),
            (2, "Store B")
        ]
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        stores = Store.view_all()

        self.assertEqual(len(stores), 2)
        self.assertEqual(stores[0][1], "Store A")
        self.assertEqual(stores[1][1], "Store B")


if __name__ == '__main__':
    unittest.main()
