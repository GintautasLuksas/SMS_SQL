import unittest
from unittest.mock import patch, MagicMock
import os
from src.db_engine import DBEngine

class TestDBEngine(unittest.TestCase):

    @patch('src.db_engine.psycopg2.connect')
    @patch('src.db_engine.logging.getLogger')
    @patch.dict(os.environ, {
        'DB_NAME': 'test_db_name',
        'DB_USERNAME': 'test_db_user',
        'DB_PASSWORD': 'test_db_password',
        'HOST': 'test_db_host',
        'PORT': 'test_db_port'
    })
    def test_connect_success(self, mock_get_logger, mock_connect):
        # Setup mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Setup mock psycopg2 connection
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Instantiate DBEngine with the mock logger
        db_engine = DBEngine(logger=mock_logger)

        # Check if psycopg2.connect was called with the correct parameters
        mock_connect.assert_called_once_with(
            dbname='test_db_name',
            user='test_db_user',
            password='test_db_password',
            host='test_db_host',
            port='test_db_port'
        )

        # Check if logging was done
        mock_logger.info.assert_called_once_with('Database connection established.')

    @patch('src.db_engine.psycopg2.connect', side_effect=Exception('Connection failed'))
    @patch('src.db_engine.logging.getLogger')
    def test_connect_failure(self, mock_get_logger, mock_connect):
        # Setup mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Expect the Exception to be raised
        with self.assertRaises(Exception):
            DBEngine(logger=mock_logger)

        # Check logging of the error
        mock_logger.error.assert_called_once_with('Error connecting to the database: Connection failed')

    @patch('src.db_engine.psycopg2.connect')
    def test_resource_cleanup(self, mock_connect):
        # Setup mock objects
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Instantiate and delete DBEngine object
        db_engine = DBEngine()
        del db_engine

        # Check if cursor and connection are closed
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
