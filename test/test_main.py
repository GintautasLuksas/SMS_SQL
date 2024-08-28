import unittest
from unittest.mock import patch
from io import StringIO
from src.main import main_menu, store_menu, people_menu, product_menu, structure_menu

class TestMainMenu(unittest.TestCase):
    """
    Unit tests for menu functions in the src.main module.
    """

    @patch('builtins.input', side_effect=['1', '1', '2', '3', '4', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('src.main.sys.exit')
    def test_main_menu(self, mock_exit, mock_stdout, mock_input):
        """
        Test the main_menu function.

        This test simulates user inputs to navigate through the main menu options. It verifies
        that the expected menu options are printed to the standard output and that the function
        eventually exits the application as expected.

        Args:
            mock_exit (MagicMock): Mocked sys.exit function.
            mock_stdout (StringIO): Mocked standard output to capture printed text.
            mock_input (MagicMock): Mocked built-in input function to simulate user choices.
        """
        main_menu()

        output = mock_stdout.getvalue()
        self.assertIn("Store Menu", output)
        self.assertIn("Manage Stores", output)
        self.assertIn("Manage Store Products", output)
        self.assertIn("Back", output)
        self.assertIn("People Menu", output)
        self.assertIn("Manage Managers", output)
        self.assertIn("Manage Workers", output)
        self.assertIn("Manage Store Managers", output)
        self.assertIn("Product Menu", output)
        self.assertIn("Manage Dry Storage Items", output)
        self.assertIn("Manage Food Items", output)
        self.assertIn("Exiting the application.", output)

    @patch('src.main.manage_store_menu')  # Mock the store menu function
    @patch('src.main.manage_store_items_menu')  # Mock the store items menu function
    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_store_menu(self, mock_input, mock_manage_store_menu, mock_manage_store_items_menu):
        """
        Test the store_menu function.

        This test simulates user inputs for navigating through the store menu. It ensures that
        the store menu and store items menu functions are called correctly based on user input.

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
    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_people_menu(self, mock_input, mock_manage_managers, mock_manage_workers, mock_manage_store_manager_menu):
        """
        Test the people_menu function.

        This test simulates user inputs for navigating through the people menu. It verifies that
        the functions for managing managers, workers, and store managers are called as expected.

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
    def test_product_menu(self, mock_input, mock_manage_dry_storage_items, mock_manage_food_items):
        """
        Test the product_menu function.

        This test simulates user inputs for navigating through the product menu. It ensures that
        the functions for managing dry storage items and food items are called as expected.

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
    def test_structure_menu(self, mock_input, mock_list_tables):
        """
        Test the structure_menu function.

        This test simulates user inputs for navigating through the structure menu. It verifies that
        the list_tables function is called correctly based on user input.

        Args:
            mock_input (MagicMock): Mocked built-in input function to simulate user choices.
            mock_list_tables (MagicMock): Mocked list_tables function.
        """
        structure_menu()
        mock_list_tables.assert_called_once()

if __name__ == "__main__":
    unittest.main()
