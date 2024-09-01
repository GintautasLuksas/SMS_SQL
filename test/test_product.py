import unittest
from unittest.mock import patch, MagicMock
from src.product.product import DryStorageItem, FoodItem
from src.db_engine import DBEngine
from typing import Optional

class TestDryStorageItem(unittest.TestCase):
    """Test suite for the DryStorageItem class."""

    @patch('src.product.product.DBEngine')
    def test_save_new_dry_storage_item(self, mock_db_engine: MagicMock) -> None:
        """Test saving a new dry storage item and assigning an ID.

        Verifies that a new dry storage item is saved to the database and checks if a new ID is returned.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Simulate returning new ID
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        item = DryStorageItem(name="Flour", amount=50, price=100, recipe_item=True, chemical=False, package_type="Bag")
        item.save()

        self.assertEqual(item.id, 1)
        mock_cursor.execute.assert_called_once()

    @patch('src.product.product.DBEngine')
    def test_delete_dry_storage_item(self, mock_db_engine: MagicMock) -> None:
        """Test deleting a dry storage item from the database.

        Verifies that an existing dry storage item is deleted from the database and checks if the ID is set to None.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        item = DryStorageItem(name="Flour", amount=50, price=100, recipe_item=True, chemical=False, package_type="Bag", id=1)
        item.delete()

        self.assertIsNone(item.id)
        mock_cursor.execute.assert_called_once_with('DELETE FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s', (1,))

class TestFoodItem(unittest.TestCase):
    """Test suite for the FoodItem class."""

    @patch('src.product.product.DBEngine')
    def test_view_all_food_items(self, mock_db_engine: MagicMock) -> None:
        """Test retrieving all food items from the database.

        Simulates retrieval of multiple food items from the database and checks the output list for correct entries.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Apple", 10, 5, "Cool", "2024-12-31"),
            (2, "Bread", 20, 3, "Dry", "2024-11-30")
        ]
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        items = FoodItem.view_all()

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "Apple")
        self.assertEqual(items[1].name, "Bread")

    @patch('src.product.product.DBEngine')
    def test_find_food_item_by_id(self, mock_db_engine: MagicMock) -> None:
        """Test finding a food item by ID.

        Simulates finding a food item by ID and checks if the correct item is returned with all attributes properly set.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, "Apple", 10, 5, "Cool", "2024-12-31")
        mock_db_engine.return_value.connection = mock_connection
        mock_db_engine.return_value.cursor = mock_cursor

        item: Optional[FoodItem] = FoodItem.find_by_id(1)

        self.assertIsNotNone(item)
        if item:
            self.assertEqual(item.name, "Apple")
            self.assertEqual(item.amount, 10)
            self.assertEqual(item.price, 5)
            self.assertEqual(item.storage_condition, "Cool")
            self.assertEqual(item.expiry_date, "2024-12-31")

if __name__ == '__main__':
    unittest.main()
