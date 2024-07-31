import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from src.db_engine import DBEngine


@patch('src.db_engine.psycopg2.connect')
def test_db_engine_init(mock_connect):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    db_engine = DBEngine()

    mock_connect.assert_called_once_with(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('HOST'),
        port=os.getenv('PORT')
    )
    assert db_engine.connection == mock_connection
    assert db_engine.cursor == mock_cursor

@patch('src.db_engine.psycopg2.connect')
def test_db_engine_del(mock_connect):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    db_engine = DBEngine()

    db_engine.__del__()

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()
