import unittest
from unittest.mock import patch, MagicMock
from src.main import main_menu, product_menu, store_menu, structure_menu, people_menu

class TestMainMenu(unittest.TestCase):
    """Unit tests for menu functions in the src.main module."""

    @patch('src.main.manage_store_menu')
    @patch('src.main.manage_store_items_menu')
    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_store_menu(self, mock_input: MagicMock, mock_manage_store_menu: MagicMock, mock_manage_store_items_menu: MagicMock) -> None:
        """Test the store_menu function.

        Args:
            mock_input (MagicMock): Mocked built-in input function to simulate user choices.
            mock_manage_store_menu (MagicMock): Mocked manage_store_menu function.
            mock_manage_store_items_menu (MagicMock): Mocked manage_store_items_menu function.
        """
        store_menu()
        mock_manage_store_menu.assert_called_once()
        mock_manage_store_items_menu.assert_called_once()

    @patch('src.main.Manager.manage_managers')
    @patch('src.main.Worker.manage_workers')
    @patch('src.main.manage_store_manager_menu')
    @patch('builtins.input', side_effect=['1', '2', '3', '4'])
    def test_people_menu(self, mock_input: MagicMock, mock_manage_managers: MagicMock, mock_manage_workers: MagicMock, mock_manage_store_manager_menu: MagicMock) -> None:
        """Test the people_menu function.

        Args:
            mock_input (MagicMock): Mocked built-in input function to simulate user choices.
            mock_manage_managers (MagicMock): Mocked manage_managers function.
            mock_manage_workers (MagicMock): Mocked manage_workers function.
            mock_manage_store_manager_menu (MagicMock): Mocked manage_store_manager_menu function.
        """
        people_menu()
        mock_manage_managers.assert_called_once()
        mock_manage_workers.assert_called_once()
        mock_manage_store_manager_menu.assert_called_once()

    @patch('src.main.manage_dry_storage_items')
    @patch('src.main.manage_food_items')
    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_product_menu(self, mock_input: MagicMock, mock_manage_dry_storage_items: MagicMock, mock_manage_food_items: MagicMock) -> None:
        """Test the product_menu function.

        Args:
            mock_input (MagicMock): Mocked built-in input function to simulate user choices.
            mock_manage_dry_storage_items (MagicMock): Mocked manage_dry_storage_items function.
            mock_manage_food_items (MagicMock): Mocked manage_food_items function.
        """
        product_menu()
        mock_manage_dry_storage_items.assert_called_once()
        mock_manage_food_items.assert_called_once()

    @patch('src.main.list_tables')
    @patch('builtins.input', side_effect=['4', '5'])
    def test_structure_menu(self, mock_input: MagicMock, mock_list_tables: MagicMock) -> None:
        """Test the structure_menu function.

        Args:
            mock_input (MagicMock): Mocked built-in input function to simulate user choices.
            mock_list_tables (MagicMock): Mocked list_tables function.
        """
        structure_menu()
        mock_list_tables.assert_called_once()

if __name__ == "__main__":
    unittest.main()
