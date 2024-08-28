import unittest
from unittest.mock import patch, MagicMock
from src.person.storemanager import StoreManager
from typing import Optional, List, Tuple

class TestStoreManager(unittest.TestCase):

    @patch('src.person.storemanager.DBEngine')
    def test_store_manager_create(self, MockDBEngine: MagicMock) -> None:
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()
        mock_cursor.fetchone.return_value = [42]

        manager = StoreManager(name="Rūta Kazlauskaitė", phone=37061234567, email="ruta.k@pavyzdys.lt",
                               country="Lithuania", store_id=5, monthly_salary=3200, petty_cash=150)

        manager.save()

        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO "Store Manager" ("StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING "StoreManagerID"
            """,
            (5, "Rūta Kazlauskaitė", "Lithuania", "ruta.k@pavyzdys.lt", 37061234567, 3200, 150)
        )
        self.assertEqual(manager.id, 42)

    @patch('src.person.storemanager.DBEngine')
    def test_store_manager_update(self, MockDBEngine: MagicMock) -> None:
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        manager = StoreManager(name="Rūta Kazlauskaitė", phone=37061234567, email="ruta.k@pavyzdys.lt",
                               country="Lithuania", store_id=5, monthly_salary=3200, petty_cash=150, id=42)

        manager.save()

        mock_cursor.execute.assert_called_once_with(
            """
            UPDATE "Store Manager"
            SET "StoreID" = %s, "Name" = %s, "Country" = %s, "Email" = %s, "PhoneNumber" = %s, "MonthlySalary" = %s, "PettyCash" = %s
            WHERE "StoreManagerID" = %s
            """,
            (5, "Rūta Kazlauskaitė", "Lithuania", "ruta.k@pavyzdys.lt", 37061234567, 3200, 150, 42)
        )

    @patch('src.person.storemanager.DBEngine')
    def test_store_manager_delete(self, MockDBEngine: MagicMock) -> None:
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        manager = StoreManager(name="Rūta Kazlauskaitė", phone=37061234567, email="ruta.k@pavyzdys.lt",
                               country="Lithuania", store_id=5, monthly_salary=3200, petty_cash=150, id=42)

        manager.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s',
            (42,)
        )
        self.assertIsNone(manager.id)

    @patch('src.person.storemanager.DBEngine')
    def test_view_all_store_managers(self, MockDBEngine: MagicMock) -> None:
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()
        mock_cursor.fetchall.return_value = [
            (7, 5, "Tomas Šukys", "Lithuania", "tomas.s@pavyzdys.lt", 37069876543, 2800, 100)
        ]

        store_managers: List[Tuple[Optional[int], int, str, str, str, int, int, int]] = StoreManager.view_all()

        mock_cursor.execute.assert_called_once_with(
            """
            SELECT "StoreManagerID", "StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash"
            FROM "Store Manager"
            """
        )
        self.assertEqual(len(store_managers), 1)
        self.assertEqual(store_managers[0],
                         (7, 5, "Tomas Šukys", "Lithuania", "tomas.s@pavyzdys.lt", 37069876543, 2800, 100))

    @patch('src.person.storemanager.DBEngine')
    def test_display_all_salaries(self, MockDBEngine: MagicMock) -> None:
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()
        mock_cursor.fetchall.return_value = [
            (7, 5, "Tomas Šukys", "Lithuania", "tomas.s@pavyzdys.lt", 37069876543, 2800, 100)
        ]

        with patch('builtins.print') as mock_print:
            StoreManager.display_all_salaries()
            mock_print.assert_any_call("Salaries of All Store Managers:")
            mock_print.assert_any_call("ID: 7, Name: Tomas Šukys, Salary: 2800")

    @patch('src.person.storemanager.DBEngine')
    def test_manage_responsibilities(self, MockDBEngine: MagicMock) -> None:
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        with patch('builtins.input', side_effect=['13', '15', '17']):
            with patch('builtins.print') as mock_print:
                StoreManager.add_responsibility(7)
                mock_cursor.execute.assert_any_call(
                    """
                    INSERT INTO "SM Responsibilities" ("ResponsibilityID", "StoreManagerID")
                    VALUES (%s, %s)
                    """,
                    (13, 7)
                )
                mock_print.assert_any_call("Responsibility 13 added to store manager 7.")

                StoreManager.remove_responsibility(7)
                mock_cursor.execute.assert_any_call(
                    'DELETE FROM "SM Responsibilities" WHERE "ResponsibilityID" = %s AND "StoreManagerID" = %s',
                    (15, 7)
                )
                mock_print.assert_any_call("Responsibility 15 removed from store manager 7.")

                StoreManager.view_responsibilities(7)
                mock_cursor.execute.assert_any_call(
                    'SELECT "ResponsibilityID" FROM "SM Responsibilities" WHERE "StoreManagerID" = %s',
                    (7,)
                )
                mock_print.assert_any_call("Responsibilities for Store Manager ID: 7")

if __name__ == '__main__':
    unittest.main()
