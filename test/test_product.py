import pytest
from unittest.mock import patch, MagicMock
from typing import Tuple
from src.product.product import DryStorageItem, FoodItem

def normalize_sql(sql: str) -> str:
    """Utility function to normalize SQL strings by stripping unnecessary spaces."""
    return ' '.join(sql.split())

def test_add_dry_storage_item() -> None:
    """Test adding a new DryStorageItem."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor
        mock_cursor.fetchone.return_value = [1]

        item = DryStorageItem(name="Test Item", amount=10, price=100, recipe_item=True, chemical=False, package_type="Box")
        item.save()

        expected_sql = """
            INSERT INTO "Dry Storage Item" ("Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType")
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING "DryStorageItemID"
        """
        actual_sql = mock_cursor.execute.call_args[0][0]  # Get the SQL query string from the mock call
        assert normalize_sql(expected_sql) == normalize_sql(actual_sql)

        assert mock_cursor.execute.call_args[0][1] == ("Test Item", 10, 100, True, False, "Box")
        assert item.id == 1

def test_update_dry_storage_item() -> None:
    """Test updating an existing DryStorageItem."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor

        item = DryStorageItem(name="Old Item", amount=5, price=50, recipe_item=False, chemical=True, package_type="Bag", id=2)
        item.name = "Updated Item"
        item.save()

        expected_sql = """
            UPDATE "Dry Storage Item"
            SET "Name" = %s, "Amount" = %s, "Price" = %s, "RecipeItem" = %s, "Chemical" = %s, "PackageType" = %s
            WHERE "DryStorageItemID" = %s
        """
        actual_sql = mock_cursor.execute.call_args[0][0]  # Get the SQL query string from the mock call
        assert normalize_sql(expected_sql) == normalize_sql(actual_sql)

        assert mock_cursor.execute.call_args[0][1] == ("Updated Item", 5, 50, False, True, "Bag", 2)

def test_view_all_dry_storage_items() -> None:
    """Test viewing all DryStorageItems."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor
        mock_cursor.fetchall.return_value = [
            (1, "Item 1", 10, 100, True, False, "Box"),
            (2, "Item 2", 20, 200, False, True, "Bag")
        ]

        items = DryStorageItem.view_all()

        assert items is not None
        assert len(items) == 2
        assert items[0].name == "Item 1"
        assert items[1].name == "Item 2"

def test_find_by_id_dry_storage_item() -> None:
    """Test finding a DryStorageItem by ID."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor
        mock_cursor.fetchone.return_value = (1, "Item 1", 10, 100, True, False, "Box")

        item = DryStorageItem.find_by_id(1)

        assert item is not None
        assert item.name == "Item 1"
        assert item.id == 1

def test_delete_dry_storage_item() -> None:
    """Test deleting a DryStorageItem."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor

        item = DryStorageItem(name="Item to Delete", amount=5, price=50, recipe_item=False, chemical=False, package_type="Box", id=3)
        item.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s',
            (3,)
        )
        assert item.id is None

def test_add_food_item() -> None:
    """Test adding a new FoodItem."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor
        mock_cursor.fetchone.return_value = [1]

        item = FoodItem(name="Test Food", amount=10, price=200, storage_condition="Cool", expiry_date="2025-01-01")
        item.save()

        expected_sql = """
            INSERT INTO "Food Item" ("Name", "Amount", "Price", "StorageCondition", "ExpiryDate")
            VALUES (%s, %s, %s, %s, %s)
            RETURNING "FoodItemID"
        """
        actual_sql = mock_cursor.execute.call_args[0][0]  # Get the SQL query string from the mock call
        assert normalize_sql(expected_sql) == normalize_sql(actual_sql)

        assert mock_cursor.execute.call_args[0][1] == ("Test Food", 10, 200, "Cool", "2025-01-01")
        assert item.id == 1

def test_update_food_item() -> None:
    """Test updating an existing FoodItem."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor

        item = FoodItem(name="Old Food", amount=5, price=150, storage_condition="Warm", expiry_date="2024-12-31", id=2)
        item.name = "Updated Food"
        item.save()

        expected_sql = """
            UPDATE "Food Item"
            SET "Name" = %s, "Amount" = %s, "Price" = %s, "StorageCondition" = %s, "ExpiryDate" = %s
            WHERE "FoodItemID" = %s
        """
        actual_sql = mock_cursor.execute.call_args[0][0]  # Get the SQL query string from the mock call
        assert normalize_sql(expected_sql) == normalize_sql(actual_sql)

        assert mock_cursor.execute.call_args[0][1] == ("Updated Food", 5, 150, "Warm", "2024-12-31", 2)

def test_view_all_food_items() -> None:
    """Test viewing all FoodItems."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor
        mock_cursor.fetchall.return_value = [
            (1, "Food 1", 10, 200, "Cool", "2025-01-01"),
            (2, "Food 2", 20, 300, "Warm", "2024-12-31")
        ]

        items = FoodItem.view_all()

        assert items is not None
        assert len(items) == 2
        assert items[0].name == "Food 1"
        assert items[1].name == "Food 2"

def test_find_by_id_food_item() -> None:
    """Test finding a FoodItem by ID."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor
        mock_cursor.fetchone.return_value = (1, "Food 1", 10, 200, "Cool", "2025-01-01")

        item = FoodItem.find_by_id(1)

        assert item is not None
        assert item.name == "Food 1"
        assert item.id == 1

def test_delete_food_item() -> None:
    """Test deleting a FoodItem."""
    with patch('src.product.product.DBEngine') as mock_db_engine:
        mock_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_instance
        mock_cursor = mock_instance.cursor

        item = FoodItem(name="Food to Delete", amount=5, price=150, storage_condition="Warm", expiry_date="2024-12-31", id=3)
        item.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Food Item" WHERE "FoodItemID" = %s',
            (3,)
        )
        assert item.id is None
