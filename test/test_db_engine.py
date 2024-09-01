import unittest
from unittest.mock import patch, MagicMock
from src.db_engine import DBEngine

class TestDBEngine(unittest.TestCase):
    """Test suite for the DBEngine class."""

    @patch('src.db_engine.psycopg2.connect')
    def test_connection_established(self, mock_connect: MagicMock) -> None:
        """Test that a connection is established when DBEngine is initialized.

        Args:
            mock_connect (MagicMock): Mock object for psycopg2.connect.

        Asserts:
            - The connection object is not None.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db = DBEngine()
        self.assertIsNotNone(db.connection)
        self.assertIsNotNone(db.cursor)

    @patch('src.db_engine.psycopg2.connect')
    def test_connection_closed(self, mock_connect: MagicMock) -> None:
        """Test that the connection and cursor are properly closed.

        Args:
            mock_connect (MagicMock): Mock object for psycopg2.connect.

        Asserts:
            - The connection close method is called once.
            - The cursor close method is called once.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db = DBEngine()
        if db.connection:
            db.connection.close()
            mock_conn.close.assert_called_once()

        if db.cursor:
            db.cursor.close()
            mock_cursor.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
