import os
import sys
import psycopg2

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class StoreManagerTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Store Manager"'  # Correctly use the table name with spaces

    def create_table(self):
        """Create the Store Manager table if it doesn't exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Store Manager" (
            "StoreManagerID" SERIAL PRIMARY KEY,
            "StoreID" INT NOT NULL,
            "Name" VARCHAR(255) NOT NULL,
            "Country" VARCHAR(255) NOT NULL,
            "Email" VARCHAR(255) NOT NULL,
            "PhoneNumber" BIGINT NOT NULL,
            "SMResponsibilityID" INT NOT NULL,
            "MonthlySalary" INT NOT NULL,
            "PettyCash" INT NOT NULL
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        """Insert a new store manager into the table."""
        insert_query = '''
        INSERT INTO "Store Manager" ("StoreID", "Name", "Country", "Email", "PhoneNumber", "SMResponsibilityID", "MonthlySalary", "PettyCash")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, store_manager_id, new_values):
        """Update an existing store manager's information."""
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Store Manager" SET {set_clause} WHERE "StoreManagerID" = %s'
        values = list(new_values.values()) + [store_manager_id]
        self._execute_query(update_query, values)

    def delete_data(self, store_manager_id):
        """Delete a store manager from the table."""
        delete_query = 'DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s'
        self._execute_query(delete_query, (store_manager_id,))

    def select_all(self):
        """Select all store managers from the table."""
        select_query = 'SELECT * FROM "Store Manager"'
        self.db_engine.cursor.execute(select_query)
        return self.db_engine.cursor.fetchall()

    def _execute_query(self, query, params=None):
        """Execute a query using the database engine's cursor."""
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
        """Add a new store manager to the table."""
        try:
            store_id = int(input("Enter store ID: "))
            name = input("Enter store manager's name: ")
            country = input("Enter store manager's country: ")
            email = input("Enter store manager's email: ")
            phone_number = int(input("Enter store manager's phone number: "))
            sm_responsibility_id = int(input("Enter store manager's responsibility ID: "))
            monthly_salary = int(input("Enter store manager's monthly salary: "))
            petty_cash = int(input("Enter store manager's petty cash: "))

            self.insert_data((store_id, name, country, email, phone_number, sm_responsibility_id, monthly_salary, petty_cash))
            print("Store Manager added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store manager: {e}")

    def edit_store_manager(self):
        """Edit an existing store manager's information."""
        try:
            store_manager_id = int(input("Enter the store manager ID to edit: "))
            store_id = input("Enter new store ID (leave empty to keep current): ")
            name = input("Enter new name (leave empty to keep current): ")
            country = input("Enter new country (leave empty to keep current): ")
            email = input("Enter new email (leave empty to keep current): ")
            phone_number = input("Enter new phone number (leave empty to keep current): ")
            sm_responsibility_id = input("Enter new responsibility ID (leave empty to keep current): ")
            monthly_salary = input("Enter new monthly salary (leave empty to keep current): ")
            petty_cash = input("Enter new petty cash (leave empty to keep current): ")

            # Collect only fields that are not empty
            new_values = {}
            if store_id:
                new_values['StoreID'] = int(store_id)
            if name:
                new_values['Name'] = name
            if country:
                new_values['Country'] = country
            if email:
                new_values['Email'] = email
            if phone_number:
                new_values['PhoneNumber'] = int(phone_number)
            if sm_responsibility_id:
                new_values['SMResponsibilityID'] = int(sm_responsibility_id)
            if monthly_salary:
                new_values['MonthlySalary'] = int(monthly_salary)
            if petty_cash:
                new_values['PettyCash'] = int(petty_cash)

            if new_values:
                self.update_data(store_manager_id, new_values)
                print("Store Manager updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating store manager: {e}")

    def delete_store_manager(self):
        """Delete a store manager from the table."""
        try:
            store_manager_id = int(input("Enter the store manager ID to delete: "))
            self.delete_data(store_manager_id)
            print("Store Manager deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store manager: {e}")

    def view_store_managers(self):
        """View all store managers in the table."""
        try:
            store_managers = self.select_all()
            if store_managers:
                print("\nStore Managers in the table:")
                for manager in store_managers:
                    print(manager)
            else:
                print("No store managers found.")
        except Exception as e:
            print(f"Error retrieving store managers: {e}")

    def manage_store_managers(self):
        """Manage store managers with add, edit, delete, and view options."""
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
