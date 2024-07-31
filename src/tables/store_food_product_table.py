import os
import sys
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class StoreFoodProductTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"StoreFoodProduct"'

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "StoreFoodProduct" (
            "StoreID" INT NOT NULL,
            "FoodProductID" INT NOT NULL,
            "Quantity" INT NOT NULL,
            FOREIGN KEY ("StoreID") REFERENCES "Store" ("StoreID"),
            FOREIGN KEY ("FoodProductID") REFERENCES "Food" ("FoodProductID")
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "StoreFoodProduct" ("StoreID", "FoodProductID", "Quantity")
        VALUES (%s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, store_id, food_product_id, new_values):
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "StoreFoodProduct" SET {set_clause} WHERE "StoreID" = %s AND "FoodProductID" = %s'
        values = list(new_values.values()) + [store_id, food_product_id]
        self._execute_query(update_query, values)

    def delete_data(self, store_id, food_product_id):
        delete_query = 'DELETE FROM "StoreFoodProduct" WHERE "StoreID" = %s AND "FoodProductID" = %s'
        self._execute_query(delete_query, (store_id, food_product_id))

    def select_all(self):
        select_query = 'SELECT * FROM "StoreFoodProduct"'
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

    def add_entry(self):
        try:
            store_id = int(input("Enter store ID: "))
            food_product_id = int(input("Enter food product ID: "))
            quantity = int(input("Enter quantity: "))

            self.insert_data((store_id, food_product_id, quantity))
            print("Store food product entry added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store food product entry: {e}")

    def edit_entry(self):
        try:
            store_id = int(input("Enter store ID: "))
            food_product_id = int(input("Enter food product ID: "))

            quantity = input("Enter new quantity (leave empty to keep current): ")

            new_values = {}
            if quantity:
                new_values['Quantity'] = int(quantity)

            if new_values:
                self.update_data(store_id, food_product_id, new_values)
                print("Store food product entry updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating store food product entry: {e}")

    def delete_entry(self):
        try:
            store_id = int(input("Enter store ID: "))
            food_product_id = int(input("Enter food product ID: "))
            self.delete_data(store_id, food_product_id)
            print("Store food product entry deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store food product entry: {e}")

    def view_entries(self):
        try:
            entries = self.select_all()
            if entries:
                print("\nStore Food Product entries:")
                for entry in entries:
                    print(entry)
            else:
                print("No store food product entries found.")
        except Exception as e:
            print(f"Error retrieving store food product entries: {e}")

    def manage_entries(self):
        while True:
            print("\nStore Food Product Management")
            print("1. Add Entry")
            print("2. Edit Entry")
            print("3. Delete Entry")
            print("4. View All Entries")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_entry()
            elif choice == '2':
                self.edit_entry()
            elif choice == '3':
                self.delete_entry()
            elif choice == '4':
                self.view_entries()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
