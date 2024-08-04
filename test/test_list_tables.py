import unittest
from unittest.mock import MagicMock, patch, call
from src.list_tables import list_tables  # Import the function from src.list_tables.py
import logging

# Set up logging for testing purposes
logging.basicConfig(level=logging.DEBUG)


class TestListTables(unittest.TestCase):

    @patch('src.list_tables.DBEngine')  # Mock DBEngine in src.list_tables
    @patch('builtins.print')
    def test_list_tables(self, mock_print, MockDBEngine):
        # Mock the DBEngine and cursor
        mock_db_engine = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db_engine.cursor = mock_cursor

        # Set up the cursor mock to return a list of tables
        mock_cursor.fetchall.return_value = [('table1',), ('table2',)]

        # Call the function to test
        list_tables()

        # Expected print calls
        expected_calls = [
            call("Tables in the database:"),
            call('table1'),
            call('table2')
        ]

        # Assert that print was called with the expected calls
        mock_print.assert_has_calls(expected_calls)

        # Ensure that the cursor's close method was called
        mock_cursor.close.assert_called_once()
        # Ensure that the DBEngine connection's close method was called
        mock_db_engine.connection.close.assert_called_once()

    @patch('src.list_tables.DBEngine')  # Mock DBEngine in src.list_tables
    @patch('builtins.print')
    @patch('src.list_tables.logger')  # Mock logger in src.list_tables
    def test_list_tables_error_handling(self, mock_logger, mock_print, MockDBEngine):
        # Mock the DBEngine and cursor
        mock_db_engine = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db_engine.cursor = mock_cursor

        # Simulate an error during cursor execution
        mock_cursor.execute.side_effect = Exception('Database error')

        # Call the function to test
        list_tables()

        # Check if logger.error was called with the expected error message
        mock_logger.error.assert_called_once_with('Error retrieving tables: Database error')

        # Ensure that the cursor's close method was called
        mock_cursor.close.assert_called_once()
        # Ensure that the DBEngine connection's close method was called
        mock_db_engine.connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
