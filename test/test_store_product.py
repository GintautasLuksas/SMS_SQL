"""
Unit tests for the `StoreDryProduct` and `StoreFoodProduct` classes in `store_product.py`.

This script tests the functionality of adding, removing, and viewing products in a store,
ensuring correct interactions with the database.

Pre-commit best practices:
- Ensure imports are sorted and used properly.
- Include clear, concise docstrings for each test case.
- Avoid long lines and enforce PEP8 compliance.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.store.store_product import StoreDryProduct, StoreFoodProduct


class TestStoreDryProduct(unittest.TestCase):
    """
    Test suite for the `StoreDryProduct` class.
    """

    @patch('src.store.store_product.DBEngine')
    def test_add_dry_storage_item_to_store(self, mock_db_engine):
        """
        Test adding a dry storage item to a store.

        Verifies that the item is correctly added to the database.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreDryProduct.add(store_id=1, dry_storage_id=2)

        mock_cursor.execute.assert_called_once_with(
            """
                        INSERT INTO "StoreDryProduct" ("StoreID", "DryStorageID")
                        VALUES (%s, %s)
                    """,
            (1, 2)
        )

    @patch('src.store.store_product.DBEngine')
    def test_remove_dry_storage_item_from_store(self, mock_db_engine):
        """
        Test removing a dry storage item from a store.

        Verifies that the item is correctly removed from the database.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreDryProduct.remove(store_id=1, dry_storage_id=2)

        mock_cursor.execute.assert_called_once_with(
            """
                        DELETE FROM "StoreDryProduct"
                        WHERE "StoreID" = %s AND "DryStorageID" = %s
                    """,
            (1, 2)
        )

    @patch('src.store.store_product.DBEngine')
    def test_view_dry_storage_items_in_store(self, mock_db_engine):
        """
        Test viewing dry storage items in a store.

        Verifies that the correct items are retrieved from the database.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Flour", 50, 100.0, "True", "False", "Bag"),
            (2, "Sugar", 30, 60.0, "False", "False", "Box")
        ]
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        items = StoreDryProduct.view(store_id=1)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0], (1, "Flour", 50, 100.0, "True", "False", "Bag"))
        self.assertEqual(items[1], (2, "Sugar", 30, 60.0, "False", "False", "Box"))


class TestStoreFoodProduct(unittest.TestCase):
    """
    Test suite for the `StoreFoodProduct` class.
    """

    @patch('src.store.store_product.DBEngine')
    def test_add_food_item_to_store(self, mock_db_engine):
        """
        Test adding a food item to a store.

        Verifies that the item is correctly added to the database.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreFoodProduct.add(store_id=1, food_id=2)

        mock_cursor.execute.assert_called_once_with(
            """
                        INSERT INTO "StoreFoodProduct" ("StoreID", "FoodID")
                        VALUES (%s, %s)
                    """,
            (1, 2)
        )

    @patch('src.store.store_product.DBEngine')
    def test_remove_food_item_from_store(self, mock_db_engine):
        """
        Test removing a food item from a store.

        Verifies that the item is correctly removed from the database.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        StoreFoodProduct.remove(store_id=1, food_id=2)

        mock_cursor.execute.assert_called_once_with(
            """
                        DELETE FROM "StoreFoodProduct"
                        WHERE "StoreID" = %s AND "FoodID" = %s
                    """,
            (1, 2)
        )

    @patch('src.store.store_product.DBEngine')
    def test_view_food_items_in_store(self, mock_db_engine):
        """
        Test viewing food items in a store.

        Verifies that the correct items are retrieved from the database.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Apple", 10, 5.0, "Cool", "2024-12-31"),
            (2, "Bread", 20, 3.0, "Dry", "2024-11-30")
        ]
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        items = StoreFoodProduct.view(store_id=1)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0], (1, "Apple", 10, 5.0, "Cool", "2024-12-31"))
        self.assertEqual(items[1], (2, "Bread", 20, 3.0, "Dry", "2024-11-30"))


if __name__ == '__main__':
    unittest.main()
