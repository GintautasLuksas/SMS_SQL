import os
import sys
import psycopg2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db_engine import DBEngine

class StoreFoodProductTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"StoreFoodProduct"'
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "StoreFoodProduct" (
            "FoodStorageID" INT NOT NULL,
            "StoreID" INT NOT NULL,
            "FoodID" INT NOT NULL,
            PRIMARY KEY ("FoodStorageID", "StoreID", "FoodID")
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "StoreFoodProduct" ("FoodStorageID", "StoreID", "FoodID")
        VALUES (%s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def delete_data(self, food_storage_id, store_id, food_id):
        delete_query = 'DELETE FROM "StoreFoodProduct" WHERE "FoodStorageID" = %s AND "StoreID" = %s AND "FoodID" = %s'
        self._execute_query(delete_query, (food_storage_id, store_id, food_id))

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

    def add_store_food_product(self):
        try:
            food_storage_id = int(input("Enter food storage ID: "))
            store_id = int(input("Enter store ID: "))
            food_id = int(input("Enter food ID: "))

            self.insert_data((food_storage_id, store_id, food_id))
            print("Store food product added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store food product: {e}")

    def delete_store_food_product(self):
        try:
            food_storage_id = int(input("Enter food storage ID to delete: "))
            store_id = int(input("Enter store ID to delete: "))
            food_id = int(input("Enter food ID to delete: "))

            self.delete_data(food_storage_id, store_id, food_id)
            print("Store food product deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store food product: {e}")

    def view_store_food_products(self):
        try:
            store_food_products = self.select_all()
            if store_food_products:
                print("\nStore Food Products:")
                for store_food_product in store_food_products:
                    print(store_food_product)
            else:
                print("No store food products found.")
        except Exception as e:
            print(f"Error retrieving store food products: {e}")

    def manage_store_food_products(self):
        while True:
            print("\nStore Food Product Management")
            print("1. Add Store Food Product")
            print("2. Delete Store Food Product")
            print("3. View All Store Food Products")
            print("4. Back")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_store_food_product()
            elif choice == '2':
                self.delete_store_food_product()
            elif choice == '3':
                self.view_store_food_products()
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")
