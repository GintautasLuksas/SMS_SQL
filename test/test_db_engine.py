import unittest
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv  # Import the dotenv function
from src.db_engine import DBEngine

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

class TestDBEngine(unittest.TestCase):

    @patch('src.db_engine.psycopg2.connect')
    @patch('src.db_engine.logging.getLogger')
    @patch.dict(os.environ, {
        'DB_NAME': 'test_db_name',
        'DB_USERNAME': 'test_db_user',
        'DB_PASSWORD': 'test_db_password',
        'HOST': 'test_db_host',
        'PORT': '5432'
    })
    def test_connect_success(self, mock_get_logger, mock_connect):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db_engine = DBEngine(logger=mock_logger)

        mock_connect.assert_called_once_with(
            dbname='test_db_name',
            user='test_db_user',
            password='test_db_password',
            host='test_db_host',
            port='5432'
        )

        mock_logger.info.assert_called_once_with('Database connection established.')

        db_engine.cursor.close()
        db_engine.connection.close()

    @patch('src.db_engine.psycopg2.connect', side_effect=Exception('Connection failed'))
    @patch('src.db_engine.logging.getLogger')
    def test_connect_failure(self, mock_get_logger, mock_connect):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with self.assertRaises(Exception):
            DBEngine(logger=mock_logger)

        mock_logger.error.assert_called_once_with('Error connecting to the database: Connection failed')

    @patch('src.db_engine.psycopg2.connect')
    def test_resource_cleanup(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        db_engine = DBEngine()
        del db_engine

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
