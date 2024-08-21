import unittest
from unittest.mock import patch
from io import StringIO


from src.main import main_menu, store_menu, people_menu, product_menu, structure_menu


class TestMainMenu(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '1', '2', '3', '4', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('src.main.sys.exit')
    def test_main_menu(self, mock_exit, mock_stdout, mock_input):
        """Test the main menu function."""
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
        """Test the store menu function."""
        store_menu()
        mock_manage_store_menu.assert_called_once()
        mock_manage_store_items_menu.assert_called_once()

    @patch('src.main.Manager.manage_managers')
    @patch('src.main.Worker.manage_workers')
    @patch('src.main.manage_store_manager_menu')
    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_people_menu(self, mock_input, mock_manage_managers, mock_manage_workers, mock_manage_store_manager_menu):
        """Test the people menu function."""
        people_menu()
        mock_manage_managers.assert_called_once()
        mock_manage_workers.assert_called_once()
        mock_manage_store_manager_menu.assert_called_once()

    @patch('src.main.manage_dry_storage_items')
    @patch('src.main.manage_food_items')
    @patch('builtins.input', side_effect=['1', '2', '3'])
    def test_product_menu(self, mock_input, mock_manage_dry_storage_items, mock_manage_food_items):
        """Test the product menu function."""
        product_menu()
        mock_manage_dry_storage_items.assert_called_once()
        mock_manage_food_items.assert_called_once()

    @patch('src.main.list_tables')
    @patch('builtins.input', side_effect=['4', '5'])
    def test_structure_menu(self, mock_input, mock_list_tables):
        """Test the structure menu function."""
        structure_menu()
        mock_list_tables.assert_called_once()


if __name__ == "__main__":
    unittest.main()
