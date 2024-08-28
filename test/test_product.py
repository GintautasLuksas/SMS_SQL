import unittest
from unittest.mock import patch, MagicMock
from src.db_engine import DBEngine
from src.product.product import Product, DryStorageItem, FoodItem

class TestProduct(unittest.TestCase):
    """
    Unit tests for the Product class.
    """

    @patch('src.db_engine.DBEngine')
    def test_product_initialization(self, MockDBEngine):
        """
        Test the initialization of the Product class.

        This test verifies that a Product object is correctly initialized with the given
        attributes and that the `id` attribute is set to None upon creation.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
        product = Product(name="Test Product", amount=10, price=100)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.amount, 10)
        self.assertEqual(product.price, 100)
        self.assertIsNone(product.id)

class TestDryStorageItem(unittest.TestCase):
    """
    Unit tests for the DryStorageItem class.
    """

    @patch('src.db_engine.DBEngine')
    def test_dry_storage_item_save(self, MockDBEngine):
        """
        Test saving a DryStorageItem to the database.

        This test ensures that the `save` method of the DryStorageItem class executes the correct
        SQL query to insert a new record into the "Dry Storage Item" table and updates the
        `id` attribute of the item based on the returned ID from the database.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
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
        """
        Test deleting a DryStorageItem from the database.

        This test verifies that the `delete` method of the DryStorageItem class executes the correct
        SQL query to delete a record from the "Dry Storage Item" table based on the `id` attribute
        of the item and sets the `id` attribute to None after deletion.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
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
        """
        Test retrieving all DryStorageItems from the database.

        This test verifies that the `view_all` class method of DryStorageItem correctly retrieves
        and returns a list of DryStorageItem instances based on the records in the database.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchall.return_value = [(1, "Test Item", 5, 50, True, False, "Box")]

        items = DryStorageItem.view_all()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Item")

class TestFoodItem(unittest.TestCase):
    """
    Unit tests for the FoodItem class.
    """

    @patch('src.db_engine.DBEngine')
    def test_food_item_save(self, MockDBEngine):
        """
        Test saving a FoodItem to the database.

        This test ensures that the `save` method of the FoodItem class executes the correct
        SQL query to insert a new record into the "Food Item" table and updates the
        `id` attribute of the item based on the returned ID from the database.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
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
        """
        Test deleting a FoodItem from the database.

        This test verifies that the `delete` method of the FoodItem class executes the correct
        SQL query to delete a record from the "Food Item" table based on the `id` attribute
        of the item and sets the `id` attribute to None after deletion.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
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
        """
        Test retrieving all FoodItems from the database.

        This test verifies that the `view_all` class method of FoodItem correctly retrieves
        and returns a list of FoodItem instances based on the records in the database.

        Args:
            MockDBEngine (MagicMock): Mocked DBEngine class to avoid actual database interactions.
        """
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
