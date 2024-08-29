"""
Unit tests for the `DBEngine` class in the `db_engine.py` module.

This script tests the database connection management functionality provided by the `DBEngine` class,
ensuring that connections are correctly established, used, and closed, with proper error handling.

Pre-commit best practices:
- Ensure imports are sorted and used properly.
- Include clear, concise docstrings for each test case.
- Avoid long lines and enforce PEP8 compliance.
"""

import unittest
from unittest.mock import patch, MagicMock
import psycopg2
from src.db_engine import DBEngine


class TestDBEngine(unittest.TestCase):
    """
    Test suite for the `DBEngine` class.
    """

    @patch('psycopg2.connect')
    def test_successful_connection(self, mock_connect):
        """
        Test that a successful connection to the database is established.

        Verifies that the connection and cursor are set up correctly when `DBEngine` is initialized.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        db_engine = DBEngine()

        self.assertIsNotNone(db_engine.connection, "Database connection should not be None.")
        self.assertIsNotNone(db_engine.cursor, "Database cursor should not be None.")
        mock_connect.assert_called_once()
        mock_connection.cursor.assert_called_once()

    @patch('psycopg2.connect')
    def test_connection_error(self, mock_connect):
        """
        Test that a connection error is handled properly.

        Simulates a connection error and verifies that an exception is raised and logged.
        """
        mock_connect.side_effect = psycopg2.OperationalError("Simulated connection error")

        with self.assertRaises(psycopg2.OperationalError):
            DBEngine()

    @patch('psycopg2.connect')
    def test_connection_close(self, mock_connect):
        """
        Test that the database connection and cursor are properly closed.

        Ensures that resources are released after use.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        db_engine = DBEngine()
        db_engine.__exit__(None, None, None)  # Manually invoke the exit to simulate closing

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_context_manager(self, mock_connect):
        """
        Test the context manager functionality of `DBEngine`.

        Verifies that the database connection and cursor are correctly managed when used within a `with` statement.
        """
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        with DBEngine() as db_engine:
            self.assertIsNotNone(db_engine.connection, "Database connection should not be None inside context manager.")
            self.assertIsNotNone(db_engine.cursor, "Database cursor should not be None inside context manager.")

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
