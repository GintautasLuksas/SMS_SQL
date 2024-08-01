import os
import sys
import psycopg2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db_engine import DBEngine

class StoreDryProductTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"StoreDryProduct"'
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "StoreDryProduct" (
            "DryStoreID" INT NOT NULL,
            "StoreID" INT NOT NULL,
            "DryStorageID" INT NOT NULL,
            PRIMARY KEY ("DryStoreID", "StoreID", "DryStorageID")
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "StoreDryProduct" ("DryStoreID", "StoreID", "DryStorageID")
        VALUES (%s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def delete_data(self, dry_store_id, store_id, dry_storage_id):
        delete_query = 'DELETE FROM "StoreDryProduct" WHERE "DryStoreID" = %s AND "StoreID" = %s AND "DryStorageID" = %s'
        self._execute_query(delete_query, (dry_store_id, store_id, dry_storage_id))

    def select_all(self):
        select_query = 'SELECT * FROM "StoreDryProduct"'
        self.db_engine.cursor.execute(select_query)
        return self.db_engine.cursor.fetchall()

    def _execute_query(self, query, params=None):
        try:
            if params:
                self.db_engine.cursor.execute(query, params)
            else:
                self.db_engine.cursor.execute(query)
            self.db_engine.connection.commit()
        except (Exception, psycopg2.Error) as error:
            self.db_engine.connection.rollback()
            print(f"Error executing query: {error}")

    def add_store_dry_product(self):
        try:
            dry_store_id = int(input("Enter dry store ID: "))
            store_id = int(input("Enter store ID: "))
            dry_storage_id = int(input("Enter dry storage ID: "))

            self.insert_data((dry_store_id, store_id, dry_storage_id))
            print("Store dry product added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store dry product: {e}")

    def delete_store_dry_product(self):
        try:
            dry_store_id = int(input("Enter dry store ID to delete: "))
            store_id = int(input("Enter store ID to delete: "))
            dry_storage_id = int(input("Enter dry storage ID to delete: "))

            self.delete_data(dry_store_id, store_id, dry_storage_id)
            print("Store dry product deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store dry product: {e}")

    def view_store_dry_products(self):
        try:
            store_dry_products = self.select_all()
            if store_dry_products:
                print("\nStore Dry Products:")
                for store_dry_product in store_dry_products:
                    print(store_dry_product)
            else:
                print("No store dry products found.")
        except Exception as e:
            print(f"Error retrieving store dry products: {e}")

    def manage_store_dry_products(self):
        while True:
            print("\nStore Dry Product Management")
            print("1. Add Store Dry Product")
            print("2. Delete Store Dry Product")
            print("3. View All Store Dry Products")
            print("4. Back")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_store_dry_product()
            elif choice == '2':
                self.delete_store_dry_product()
            elif choice == '3':
                self.view_store_dry_products()
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")
