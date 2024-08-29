"""
Unit tests for the `list_tables` function in the `list_tables.py` module.

This script tests the functionality of listing database tables using the `list_tables` function,
verifying that it correctly retrieves and outputs table names, and handles errors gracefully.

Pre-commit best practices:
- Ensure imports are sorted and used properly.
- Include clear, concise docstrings for each test case.
- Avoid long lines and enforce PEP8 compliance.
"""

import unittest
from unittest.mock import patch, MagicMock
import psycopg2
from io import StringIO
from src.list_tables import list_tables

class TestListTables(unittest.TestCase):
    """
    Test suite for the `list_tables` function.
    """

    @patch('src.list_tables.DBEngine')
    def test_list_tables_no_tables(self, mock_db_engine):
        """
        Test that `list_tables` handles the scenario where no tables are present.

        Simulates an empty database and verifies that the output is appropriate.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_db_engine.return_value.__enter__.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            list_tables()
            output = mock_stdout.getvalue().strip()
            expected_output = "Tables in the database:"
            self.assertEqual(output, expected_output)

    @patch('src.list_tables.DBEngine')
    @patch('src.list_tables.logger')
    def test_list_tables_db_error(self, mock_logger, mock_db_engine):
        """
        Test that `list_tables` handles database errors gracefully.

        Simulates a database error during the execution of the SQL query.
        """
        mock_db_engine.return_value.cursor = MagicMock()
        mock_db_engine.return_value.cursor.execute.side_effect = psycopg2.Error("Simulated database error")

        list_tables()

        mock_logger.error.assert_called_once_with("Error retrieving tables: Simulated database error")

if __name__ == '__main__':
    unittest.main()
