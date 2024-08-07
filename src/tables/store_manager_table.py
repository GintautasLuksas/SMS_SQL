import os
import sys
import psycopg2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class StoreManagerTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Store Manager"'
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Store Manager" (
            "StoreManagerID" SERIAL PRIMARY KEY,
            "ManagerID" INT NOT NULL,
            "StoreID" INT NOT NULL
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "Store Manager" ("ManagerID", "StoreID")
        VALUES (%s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, store_manager_id, new_values):
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Store Manager" SET {set_clause} WHERE "StoreManagerID" = %s'
        values = list(new_values.values()) + [store_manager_id]
        self._execute_query(update_query, values)

    def delete_data(self, store_manager_id):
        delete_query = 'DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s'
        self._execute_query(delete_query, (store_manager_id,))

    def select_all(self):
        select_query = 'SELECT * FROM "Store Manager"'
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

    def add_store_manager(self):
        try:
            manager_id = int(input("Enter Store manager ID: "))
            store_id = int(input("Enter store ID: "))

            self.insert_data((manager_id, store_id))
            print("Store manager added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store manager: {e}")

    def edit_store_manager(self):
        try:
            store_manager_id = int(input("Enter the store manager ID to edit: "))
            manager_id = input("Enter new manager ID (leave empty to keep current): ")
            store_id = input("Enter new store ID (leave empty to keep current): ")

            new_values = {}
            if manager_id:
                new_values['ManagerID'] = int(manager_id)
            if store_id:
                new_values['StoreID'] = int(store_id)

            if new_values:
                self.update_data(store_manager_id, new_values)
                print("Store manager updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating store manager: {e}")

    def delete_store_manager(self):
        try:
            store_manager_id = int(input("Enter the store manager ID to delete: "))
            self.delete_data(store_manager_id)
            print("Store manager deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store manager: {e}")

    def view_store_managers(self):
        try:
            store_managers = self.select_all()
            if store_managers:
                print("\nStore Managers:")
                for store_manager in store_managers:
                    print(store_manager)
            else:
                print("No store managers found.")
        except Exception as e:
            print(f"Error retrieving store managers: {e}")

    def manage_store_managers(self):
        while True:
            print("\nStore Manager Management")
            print("1. Add Store Manager")
            print("2. Edit Store Manager")
            print("3. Delete Store Manager")
            print("4. View All Store Managers")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_store_manager()
            elif choice == '2':
                self.edit_store_manager()
            elif choice == '3':
                self.delete_store_manager()
            elif choice == '4':
                self.view_store_managers()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
