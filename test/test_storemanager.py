import unittest
from unittest.mock import patch, MagicMock
from src.person.storemanager import StoreManager

class TestStoreManager(unittest.TestCase):

    @patch('src.person.store_manager.DBEngine')
    def test_store_manager_create(self, MockDBEngine):
        # Test creating a new store manager
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchone.return_value = [42]  # Simulate returning ID 42

        manager = StoreManager(name="Asta Kavaliauskaitė", phone=37061234567, email="asta.k@pavyzdys.lt",
                               country="Lithuania", store_id=5, monthly_salary=3200, petty_cash=150)

        manager.save()

        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO "Store Manager" ("StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING "StoreManagerID"
            """,
            (5, "Asta Kavaliauskaitė", "Lithuania", "asta.k@pavyzdys.lt", 37061234567, 3200, 150)
        )
        self.assertEqual(manager.id, 42)

    @patch('src.person.store_manager.DBEngine')  # Mock DBEngine in the module where StoreManager is defined
    def test_store_manager_update(self, MockDBEngine):
        # Test updating an existing store manager
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        manager = StoreManager(name="Asta Kavaliauskaitė", phone=37061234567, email="asta.k@pavyzdys.lt",
                               country="Lithuania", store_id=5, monthly_salary=3200, petty_cash=150, id=42)

        manager.save()

        mock_cursor.execute.assert_called_once_with(
            """
            UPDATE "Store Manager"
            SET "StoreID" = %s, "Name" = %s, "Country" = %s, "Email" = %s, "PhoneNumber" = %s, "MonthlySalary" = %s, "PettyCash" = %s
            WHERE "StoreManagerID" = %s
            """,
            (5, "Asta Kavaliauskaitė", "Lithuania", "asta.k@pavyzdys.lt", 37061234567, 3200, 150, 42)
        )

    @patch('src.person.store_manager.DBEngine')  # Mock DBEngine in the module where StoreManager is defined
    def test_store_manager_delete(self, MockDBEngine):
        # Test deleting a store manager
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        manager = StoreManager(name="Asta Kavaliauskaitė", phone=37061234567, email="asta.k@pavyzdys.lt",
                               country="Lithuania", store_id=5, monthly_salary=3200, petty_cash=150, id=42)

        manager.delete()

        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s',
            (42,)
        )
        self.assertIsNone(manager.id)

    @patch('src.person.store_manager.DBEngine')  # Mock DBEngine in the module where StoreManager is defined
    def test_view_all_store_managers(self, MockDBEngine):
        # Test viewing all store managers
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchall.return_value = [
            (7, 5, "Dainius Šukys", "Lithuania", "dainius.s@pavyzdys.lt", 37069876543, 2800, 100)
        ]

        store_managers = StoreManager.view_all()

        mock_cursor.execute.assert_called_once_with(
            """
            SELECT "StoreManagerID", "StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash"
            FROM "Store Manager"
            """
        )
        self.assertEqual(len(store_managers), 1)
        self.assertEqual(store_managers[0], (7, 5, "Dainius Šukys", "Lithuania", "dainius.s@pavyzdys.lt", 37069876543, 2800, 100))

    @patch('src.person.store_manager.DBEngine')  # Mock DBEngine in the module where StoreManager is defined
    def test_display_all_salaries(self, MockDBEngine):
        # Test displaying all store managers' salaries
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        mock_cursor.fetchall.return_value = [
            (7, 5, "Dainius Šukys", "Lithuania", "dainius.s@pavyzdys.lt", 37069876543, 2800, 100)
        ]

        with patch('builtins.print') as mock_print:
            StoreManager.display_all_salaries()
            mock_print.assert_any_call("Salaries of All Store Managers:")
            mock_print.assert_any_call("ID: 7, Name: Dainius Šukys, Salary: 2800")

    @patch('src.person.store_manager.DBEngine')  # Mock DBEngine in the module where StoreManager is defined
    def test_manage_responsibilities(self, MockDBEngine):
        # Test managing responsibilities (Add and Remove)
        mock_db = MockDBEngine.return_value
        mock_cursor = MagicMock()
        mock_db.cursor = mock_cursor
        mock_db.connection = MagicMock()

        # Mock input and output for add and remove responsibilities
        with patch('builtins.input', side_effect=['13', '15', '17']) as mock_input:
            with patch('builtins.print') as mock_print:
                StoreManager.add_responsibility(7)
                mock_cursor.execute.assert_called_once_with(
                    """
                    INSERT INTO "SM Responsibilities" ("ResponsibilityID", "StoreManagerID")
                    VALUES (%s, %s)
                    """,
                    (13, 7)
                )
                mock_print.assert_any_call("Responsibility 13 added to store manager 7.")

                StoreManager.remove_responsibility(7)
                mock_cursor.execute.assert_called_with(
                    'DELETE FROM "SM Responsibilities" WHERE "ResponsibilityID" = %s AND "StoreManagerID" = %s',
                    (15, 7)
                )
                mock_print.assert_any_call("Responsibility 15 removed from store manager 7.")

                StoreManager.view_responsibilities(7)
                mock_cursor.execute.assert_called_with(
                    'SELECT * FROM "SM Responsibilities" WHERE "StoreManagerID" = %s',
                    (7,)
                )
                mock_print.assert_any_call("\nResponsibilities for Store Manager ID: 7")

if __name__ == '__main__':
    unittest.main()
