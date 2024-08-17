import unittest
from unittest.mock import patch, MagicMock
from src.db_engine import DBEngine
from src.product.product import Product, DryStorageItem, FoodItem  # Adjust import according to your module's name

class TestProduct(unittest.TestCase):

    @patch('src.db_engine.DBEngine')
    def test_product_initialization(self, MockDBEngine):
        # Test the initialization of Product class
        product = Product(name="Test Product", amount=10, price=100)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.amount, 10)
        self.assertEqual(product.price, 100)
        self.assertIsNone(product.id)

class TestDryStorageItem(unittest.TestCase):

    @patch('src.db_engine.DBEngine')
    def test_dry_storage_item_save(self, MockDBEngine):
        # Test saving a DryStorageItem
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        item = DryStorageItem(name="Test Item", amount=5, price=50, recipe_item=True, chemical=False, package_type="Box")

        # Simulate insertion
        mock_cursor.fetchone.return_value = [1]  # Assume ID returned is 1

        item.save()

        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO "Dry Storage Item" ("Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType")
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING "DryStorageItemID"
            """,
            ("Test Item", 5, 50, True, False, "Box")
        )
        self.assertEqual(item.id, 1)

    @patch('src.db_engine.DBEngine')
    def test_dry_storage_item_delete(self, MockDBEngine):
        # Test deleting a DryStorageItem
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        item = DryStorageItem(name="Test Item", amount=5, price=50, recipe_item=True, chemical=False, package_type="Box", id=1)

        item.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s',
            (1,)
        )
        self.assertIsNone(item.id)

    @patch('src.db_engine.DBEngine')
    def test_dry_storage_item_view_all(self, MockDBEngine):
        # Test viewing all DryStorageItems
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchall.return_value = [(1, "Test Item", 5, 50, True, False, "Box")]

        items = DryStorageItem.view_all()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Item")

class TestFoodItem(unittest.TestCase):

    @patch('src.db_engine.DBEngine')
    def test_food_item_save(self, MockDBEngine):
        # Test saving a FoodItem
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        item = FoodItem(name="Test Food", amount=10, price=150, storage_condition="Cool", expiry_date="2024-12-31")

        # Simulate insertion
        mock_cursor.fetchone.return_value = [1]  # Assume ID returned is 1

        item.save()

        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO "Food Item" ("Name", "Amount", "Price", "StorageCondition", "ExpiryDate")
            VALUES (%s, %s, %s, %s, %s)
            RETURNING "FoodItemID"
            """,
            ("Test Food", 10, 150, "Cool", "2024-12-31")
        )
        self.assertEqual(item.id, 1)

    @patch('src.db_engine.DBEngine')
    def test_food_item_delete(self, MockDBEngine):
        # Test deleting a FoodItem
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        item = FoodItem(name="Test Food", amount=10, price=150, storage_condition="Cool", expiry_date="2024-12-31", id=1)

        item.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Food Item" WHERE "FoodItemID" = %s',
            (1,)
        )
        self.assertIsNone(item.id)

    @patch('src.db_engine.DBEngine')
    def test_food_item_view_all(self, MockDBEngine):
        # Test viewing all FoodItems
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchall.return_value = [(1, "Test Food", 10, 150, "Cool", "2024-12-31")]

        items = FoodItem.view_all()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Food")

if __name__ == '__main__':
    unittest.main()
