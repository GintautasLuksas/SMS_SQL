import os
import sys
import psycopg2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db_engine import DBEngine
class StoreTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Store"'
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Store" (
            "StoreID" SERIAL PRIMARY KEY,
            "StoreName" VARCHAR(255) NOT NULL,
            "StoreManagerID" INT NOT NULL,
            "ManagerID" INT NOT NULL,
            "WorkerID" INT NOT NULL,
            "FoodStorageID" INT NOT NULL,
            "DryStoreID" INT NOT NULL
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "Store" ("StoreName", "StoreManagerID", "ManagerID", "WorkerID", "FoodStorageID", "DryStoreID")
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, store_id, new_values):
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Store" SET {set_clause} WHERE "StoreID" = %s'
        values = list(new_values.values()) + [store_id]
        self._execute_query(update_query, values)

    def delete_data(self, store_id):
        delete_query = 'DELETE FROM "Store" WHERE "StoreID" = %s'
        self._execute_query(delete_query, (store_id,))

    def select_all(self):
        select_query = 'SELECT * FROM "Store"'
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

    def add_store(self):
        try:
            store_name = input("Enter store name: ")
            store_manager_id = int(input("Enter store manager ID: "))
            manager_id = int(input("Enter manager ID: "))
            worker_id = int(input("Enter worker ID: "))
            food_storage_id = int(input("Enter food storage ID: "))
            dry_store_id = int(input("Enter dry store ID: "))

            self.insert_data((store_name, store_manager_id, manager_id, worker_id, food_storage_id, dry_store_id))
            print("Store added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store: {e}")

    def edit_store(self):
        try:
            store_id = int(input("Enter the store ID to edit: "))
            store_name = input("Enter new store name (leave empty to keep current): ")
            store_manager_id = input("Enter new store manager ID (leave empty to keep current): ")
            manager_id = input("Enter new manager ID (leave empty to keep current): ")
            worker_id = input("Enter new worker ID (leave empty to keep current): ")
            food_storage_id = input("Enter new food storage ID (leave empty to keep current): ")
            dry_store_id = input("Enter new dry store ID (leave empty to keep current): ")

            new_values = {}
            if store_name:
                new_values['StoreName'] = store_name
            if store_manager_id:
                new_values['StoreManagerID'] = int(store_manager_id)
            if manager_id:
                new_values['ManagerID'] = int(manager_id)
            if worker_id:
                new_values['WorkerID'] = int(worker_id)
            if food_storage_id:
                new_values['FoodStorageID'] = int(food_storage_id)
            if dry_store_id:
                new_values['DryStoreID'] = int(dry_store_id)

            if new_values:
                self.update_data(store_id, new_values)
                print("Store updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating store: {e}")

    def delete_store(self):
        try:
            store_id = int(input("Enter the store ID to delete: "))
            self.delete_data(store_id)
            print("Store deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store: {e}")

    def view_stores(self):
        try:
            stores = self.select_all()
            if stores:
                print("\nStores:")
                for store in stores:
                    print(store)
            else:
                print("No stores found.")
        except Exception as e:
            print(f"Error retrieving stores: {e}")

    def manage_stores(self):
        while True:
            print("\nStore Management")
            print("1. Add Store")
            print("2. Edit Store")
            print("3. Delete Store")
            print("4. View All Stores")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_store()
            elif choice == '2':
                self.edit_store()
            elif choice == '3':
                self.delete_store()
            elif choice == '4':
                self.view_stores()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
