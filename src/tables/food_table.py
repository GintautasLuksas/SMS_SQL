import os
import sys
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class FoodTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Food"'

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Food" (
            "FoodID" SERIAL PRIMARY KEY,
            "ProductName" VARCHAR(255) NOT NULL,
            "Quantity" INT NOT NULL,
            "StoreID" INT NOT NULL
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "Food" ("ProductName", "Quantity", "StoreID")
        VALUES (%s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, food_id, new_values):
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Food" SET {set_clause} WHERE "FoodID" = %s'
        values = list(new_values.values()) + [food_id]
        self._execute_query(update_query, values)

    def delete_data(self, food_id):
        delete_query = 'DELETE FROM "Food" WHERE "FoodID" = %s'
        self._execute_query(delete_query, (food_id,))

    def select_all(self):
        select_query = 'SELECT * FROM "Food"'
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

    def add_food(self):
        try:
            product_name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            store_id = int(input("Enter store ID: "))

            self.insert_data((product_name, quantity, store_id))
            print("Food item added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding food item: {e}")

    def edit_food(self):
        try:
            food_id = int(input("Enter the Food ID to edit: "))
            product_name = input("Enter new product name (leave empty to keep current): ")
            quantity = input("Enter new quantity (leave empty to keep current): ")
            store_id = input("Enter new store ID (leave empty to keep current): ")

            new_values = {}
            if product_name:
                new_values['ProductName'] = product_name
            if quantity:
                new_values['Quantity'] = int(quantity)
            if store_id:
                new_values['StoreID'] = int(store_id)

            if new_values:
                self.update_data(food_id, new_values)
                print("Food item updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating food item: {e}")

    def delete_food(self):
        try:
            food_id = int(input("Enter the Food ID to delete: "))
            self.delete_data(food_id)
            print("Food item deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting food item: {e}")

    def view_food(self):
        try:
            food_items = self.select_all()
            if food_items:
                print("\nFood items in the table:")
                for item in food_items:
                    print(item)
            else:
                print("No food items found.")
        except Exception as e:
            print(f"Error retrieving food items: {e}")

    def manage_food(self):
        while True:
            print("\nFood Management")
            print("1. Add Food Item")
            print("2. Edit Food Item")
            print("3. Delete Food Item")
            print("4. View All Food Items")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_food()
            elif choice == '2':
                self.edit_food()
            elif choice == '3':
                self.delete_food()
            elif choice == '4':
                self.view_food()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
