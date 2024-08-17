import unittest
from unittest.mock import MagicMock, patch
from src.person.dry_storage_Item_table import DryStorageTable


class TestDryStorageTable(unittest.TestCase):

    def setUp(self):
        # Create a DryStorageTable instance with a mocked DBEngine
        self.dry_storage = DryStorageTable()
        self.dry_storage.db_engine = MagicMock()
        self.dry_storage.db_engine.connection = MagicMock()
        self.dry_storage.db_engine.cursor = MagicMock()

    def test_create_table(self):
        self.dry_storage._execute_query = MagicMock()
        self.dry_storage.create_table()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Dry Storage" (
            "DryStorageID" SERIAL PRIMARY KEY,
            "Name" VARCHAR(255) NOT NULL,
            "Amount" INT NOT NULL,
            "Price" INT NOT NULL,
            "RecipeItem" BOOLEAN NOT NULL,
            "Chemical" BOOLEAN NOT NULL,
            "PackageType" VARCHAR(255) NOT NULL
        );
        '''
        self.dry_storage._execute_query.assert_called_once_with(create_table_query)

    def test_insert_data(self):
        data = ('TestName', 10, 100, True, False, 'Box')
        self.dry_storage._execute_query = MagicMock()
        self.dry_storage.insert_data(data)
        insert_query = '''
        INSERT INTO "Dry Storage" ("Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType")
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        self.dry_storage._execute_query.assert_called_once_with(insert_query, data)

    def test_update_data(self):
        new_values = {
            'Name': 'UpdatedName',
            'Amount': 20,
            'Price': 200,
            'RecipeItem': False,
            'Chemical': True,
            'PackageType': 'Bag'
        }
        dry_storage_id = 1
        self.dry_storage._execute_query = MagicMock()
        self.dry_storage.update_data(dry_storage_id, new_values)
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Dry Storage" SET {set_clause} WHERE "DryStorageID" = %s'
        values = list(new_values.values()) + [dry_storage_id]
        self.dry_storage._execute_query.assert_called_once_with(update_query, values)

    def test_delete_data(self):
        dry_storage_id = 1
        self.dry_storage._execute_query = MagicMock()
        self.dry_storage.delete_data(dry_storage_id)
        delete_query = 'DELETE FROM "Dry Storage" WHERE "DryStorageID" = %s'
        self.dry_storage._execute_query.assert_called_once_with(delete_query, (dry_storage_id,))

    def test_select_all(self):
        self.dry_storage.db_engine.cursor.fetchall = MagicMock(return_value=[('TestName', 10, 100, True, False, 'Box')])
        self.dry_storage.select_all()
        self.dry_storage.db_engine.cursor.execute.assert_called_once_with('SELECT * FROM "Dry Storage"')

    def test_execute_query_success(self):
        self.dry_storage.db_engine.cursor.execute = MagicMock()
        self.dry_storage._execute_query('SELECT * FROM "Dry Storage"')
        self.dry_storage.db_engine.cursor.execute.assert_called_once_with('SELECT * FROM "Dry Storage"')
        self.dry_storage.db_engine.connection.commit.assert_called_once()

    def test_execute_query_failure(self):
        self.dry_storage.db_engine.cursor.execute = MagicMock(side_effect=Exception('Database error'))
        with patch('builtins.print') as mock_print:
            self.dry_storage._execute_query('SELECT * FROM "Dry Storage"')
            self.dry_storage.db_engine.connection.rollback.assert_called_once()
            mock_print.assert_called_once_with('Error executing query: Database error')


if __name__ == '__main__':
    unittest.main()
