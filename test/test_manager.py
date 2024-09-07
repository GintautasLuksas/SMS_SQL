import pytest
from unittest.mock import MagicMock, patch
from src.person.manager import Manager
from typing import Tuple


def test_create_manager() -> None:
    """Test creating a new manager."""
    with patch('src.person.manager.DBEngine') as mock_db_engine:
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.cursor.fetchone.return_value = [49]

        manager = Manager(
            name='Petras',
            phone=37064999999,
            email='petras@example.com',
            country='Latvia',
            monthly_salary=1800,
            store_id=5
        )
        manager.save()

        expected_sql = " ".join((
            "INSERT INTO \"Manager\" (\"Name\", \"PhoneNumber\", \"Email\", \"Country\", \"MonthlySalary\", \"StoreID\")",
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING \"ManagerID\""
        )).strip()

        actual_sql = " ".join(mock_db_instance.cursor.execute.call_args[0][0].split()).strip()

        assert actual_sql == expected_sql
        mock_db_instance.cursor.execute.assert_called_once_with(
            mock_db_instance.cursor.execute.call_args[0][0],
            ('Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5)
        )


def test_update_manager() -> None:
    """Test updating an existing manager."""
    with patch('src.person.manager.DBEngine') as mock_db_engine:
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance

        manager = Manager(
            name='Petras',
            phone=37064999999,
            email='petras@example.com',
            country='Latvia',
            monthly_salary=1800,
            store_id=5,
            id=49
        )
        manager.save()

        expected_sql = " ".join((
            "UPDATE \"Manager\"",
            "SET \"Name\" = %s, \"PhoneNumber\" = %s, \"Email\" = %s, \"Country\" = %s,",
            "\"MonthlySalary\" = %s, \"StoreID\" = %s",
            "WHERE \"ManagerID\" = %s"
        )).strip()

        actual_sql = " ".join(mock_db_instance.cursor.execute.call_args[0][0].split()).strip()

        assert actual_sql == expected_sql
        mock_db_instance.cursor.execute.assert_called_once_with(
            mock_db_instance.cursor.execute.call_args[0][0],
            ('Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5, 49)
        )


def test_delete_manager() -> None:
    """Test deleting a manager."""
    with patch('src.person.manager.DBEngine') as mock_db_engine:
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance

        manager = Manager(
            name='Petras',
            phone=37064999999,
            email='petras@example.com',
            country='Latvia',
            monthly_salary=1800,
            store_id=5,
            id=49
        )
        manager.delete()

        mock_db_instance.cursor.execute.assert_called_once_with(
            'DELETE FROM "Manager" WHERE "ManagerID" = %s',
            (49,)
        )
        mock_db_instance.connection.commit.assert_called_once()


def test_view_all_managers(capsys: pytest.CaptureFixture[str]) -> None:
    """Test viewing all managers."""
    with patch('src.person.manager.DBEngine') as mock_db_engine:
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.cursor.fetchall.return_value = [
            (49, 'Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5)
        ]

        Manager.view_all()

        captured = capsys.readouterr()
        assert "List of All Managers:" in captured.out
        assert "ID: 49, Name: Petras, Phone: 37064999999, Email: petras@example.com, Country: Latvia, Salary: 1800, Store ID: 5" in captured.out


def test_display_all_salaries(capsys: pytest.CaptureFixture[str]) -> None:
    """Test displaying all managers' salaries."""
    with patch('src.person.manager.DBEngine') as mock_db_engine:
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.cursor.fetchall.return_value = [
            (49, 'Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5)
        ]

        Manager.display_all_salaries()

        captured = capsys.readouterr()
        assert "List of All Managers:" in captured.out
        assert "ID: 49, Name: Petras, Phone: 37064999999, Email: petras@example.com, Country: Latvia, Salary: 1800, Store ID: 5" in captured.out
