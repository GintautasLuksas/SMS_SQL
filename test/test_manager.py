import unittest
from unittest.mock import patch, MagicMock
from src.person.manager import Manager

class TestManager(unittest.TestCase):
    """Test suite for the Manager class."""

    @patch('src.person.manager.DBEngine')
    def test_create_manager(self, mock_db_engine: MagicMock) -> None:
        """Test creating a new manager."""
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

        self.assertEqual(actual_sql, expected_sql)
        mock_db_instance.cursor.execute.assert_called_once_with(
            mock_db_instance.cursor.execute.call_args[0][0],
            ('Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5)
        )

    @patch('src.person.manager.DBEngine')
    def test_update_manager(self, mock_db_engine: MagicMock) -> None:
        """Test updating an existing manager."""
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

        self.assertEqual(actual_sql, expected_sql)
        mock_db_instance.cursor.execute.assert_called_once_with(
            mock_db_instance.cursor.execute.call_args[0][0],
            ('Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5, 49)
        )

    @patch('src.person.manager.DBEngine')
    def test_delete_manager(self, mock_db_engine: MagicMock) -> None:
        """Test deleting a manager."""
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

    @patch('src.person.manager.DBEngine')
    @patch('builtins.print')
    def test_view_all_managers(self, mock_print: MagicMock, mock_db_engine: MagicMock) -> None:
        """Test viewing all managers."""
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.cursor.fetchall.return_value = [
            (49, 'Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5)
        ]

        Manager.view_all()

        # Verify that the print function was called with the expected output
        mock_print.assert_any_call("List of Managers:")
        mock_print.assert_any_call("ID: 49, Name: Petras, Phone: 37064999999, Email: petras@example.com, Country: Latvia, Monthly Salary: 1800, Store ID: 5")

    @patch('src.person.manager.DBEngine')
    @patch('builtins.print')
    def test_display_all_salaries(self, mock_print: MagicMock, mock_db_engine: MagicMock) -> None:
        """Test displaying all managers' salaries."""
        mock_db_instance = MagicMock()
        mock_db_engine.return_value.__enter__.return_value = mock_db_instance
        mock_db_instance.cursor.fetchall.return_value = [
            (49, 'Petras', 37064999999, 'petras@example.com', 'Latvia', 1800, 5)
        ]

        Manager.display_all_salaries()

        mock_print.assert_any_call("Salaries of All Managers:")
        mock_print.assert_any_call("ID: 49, Name: Petras, Salary: 1800")

if __name__ == '__main__':
    unittest.main()
