import unittest
from unittest.mock import patch, MagicMock
from src.person.storemanager import StoreManager


class TestStoreManager(unittest.TestCase):
    """Test suite for the `StoreManager` class."""

    @patch('src.person.storemanager.DBEngine')
    def test_add_store_manager(self, mock_db_engine: MagicMock) -> None:
        """Test adding a new store manager."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [99]
        mock_db_engine.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        store_manager = StoreManager(name="Dainius Petrauskas", phone=861234567, email="dainius.petrauskas@example.lt",
                                     country="Lithuania", store_id=15, monthly_salary=4500, petty_cash=200)
        store_manager.save()

        mock_cursor.execute.assert_called_once_with(
            """
                INSERT INTO "Store Manager" ("StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "StoreManagerID"
            """,
            (15, "Dainius Petrauskas", "Lithuania", "dainius.petrauskas@example.lt", 861234567, 4500, 200)
        )
        self.assertEqual(store_manager.id, 99)

    @patch('src.person.storemanager.DBEngine')
    def test_update_store_manager(self, mock_db_engine: MagicMock) -> None:
        """Test updating an existing store manager."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        store_manager = StoreManager(name="Gintaras Vaitkus", phone=862345678, email="gintaras.vaitkus@example.lt",
                                     country="Lithuania", store_id=23, monthly_salary=5200, petty_cash=350, id=42)
        store_manager.save()

        mock_cursor.execute.assert_called_once_with(
            """
                UPDATE "Store Manager"
                SET "StoreID" = %s, "Name" = %s, "Country" = %s, "Email" = %s, "PhoneNumber" = %s, "MonthlySalary" = %s, "PettyCash" = %s
                WHERE "StoreManagerID" = %s
            """,
            (23, "Gintaras Vaitkus", "Lithuania", "gintaras.vaitkus@example.lt", 862345678, 5200, 350, 42)
        )

    @patch('src.person.storemanager.DBEngine')
    def test_delete_store_manager(self, mock_db_engine: MagicMock) -> None:
        """Test deleting a store manager."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_db_engine.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        store_manager = StoreManager(name="Rūta Žemaitė", phone=865432198, email="ruta.zemaite@example.lt",
                                     country="Lithuania", store_id=17, monthly_salary=4800, petty_cash=400, id=67)
        store_manager.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s', (67,)
        )
        self.assertIsNone(store_manager.id)

    @patch('src.person.storemanager.DBEngine')
    def test_view_all_store_managers(self, mock_db_engine: MagicMock) -> None:
        """Test viewing all store managers."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (12, 30, "Algirdas Jankauskas", "Lithuania", "algirdas.jankauskas@example.lt", 860123456, 5500, 500),
            (14, 31, "Birutė Dambrauskienė", "Lithuania", "birute.dambrauskiene@example.lt", 869876543, 6000, 600)
        ]
        mock_db_engine.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        store_managers = StoreManager.view_all()

        self.assertEqual(len(store_managers), 2)
        self.assertEqual(store_managers[0].name, "Algirdas Jankauskas")
        self.assertEqual(store_managers[1].name, "Birutė Dambrauskienė")

    @patch('src.person.storemanager.DBEngine')
    def test_display_all_salaries(self, mock_db_engine: MagicMock) -> None:
        """Test displaying all store managers' salaries."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (12, 30, "Algirdas Jankauskas", "Lithuania", "algirdas.jankauskas@example.lt", 860123456, 5500, 500),
            (14, 31, "Birutė Dambrauskienė", "Lithuania", "birute.dambrauskiene@example.lt", 869876543, 6000, 600)
        ]
        mock_db_engine.return_value = MagicMock(connection=mock_connection, cursor=mock_cursor)

        with patch('sys.stdout', new_callable=MagicMock()) as mock_stdout:
            StoreManager.display_all_salaries()

            output = ''.join(call.args[0] for call in mock_stdout.write.call_args_list)

            self.assertIn("Salaries of All Store Managers:", output)
            self.assertIn("ID: 12, Name: Algirdas Jankauskas, Salary: 5500", output)
            self.assertIn("ID: 14, Name: Birutė Dambrauskienė, Salary: 6000", output)


if __name__ == '__main__':
    unittest.main()
