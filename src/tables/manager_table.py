import os
import sys
import psycopg2

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class ManagerTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Manager"'
        self.create_table()

    def create_table(self):
        """Create the Manager table if it doesn't exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Manager" (
            "ManagerID" SERIAL PRIMARY KEY,
            "Name" VARCHAR(255) NOT NULL,
            "PhoneNumber" BIGINT NOT NULL,
            "Email" VARCHAR(255) NOT NULL,
            "Country" VARCHAR(255) NOT NULL,
            "HourlyRate" INT NOT NULL,
            "AmountWorked" INT NOT NULL
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        """Insert a new manager into the table."""
        insert_query = '''
        INSERT INTO "Manager" ("Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked")
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, manager_id, new_values):
        """Update an existing manager's information."""
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Manager" SET {set_clause} WHERE "ManagerID" = %s'
        values = list(new_values.values()) + [manager_id]
        self._execute_query(update_query, values)

    def delete_data(self, manager_id):
        """Delete a manager from the table."""
        delete_query = 'DELETE FROM "Manager" WHERE "ManagerID" = %s'
        self._execute_query(delete_query, (manager_id,))

    def select_all(self):
        """Select all managers from the table."""
        select_query = 'SELECT * FROM "Manager"'
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

    def add_manager(self):
        """Add a new manager to the table."""
        try:
            name = input("Enter manager's name: ")
            phone_number = int(input("Enter manager's phone number: "))
            email = input("Enter manager's email: ")
            country = input("Enter manager's country: ")
            hourly_rate = int(input("Enter manager's hourly rate: "))
            amount_worked = int(input("Enter amount worked: "))

            self.insert_data((name, phone_number, email, country, hourly_rate, amount_worked))
            print("Manager added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding manager: {e}")

    def edit_manager(self):
        """Edit an existing manager's information."""
        try:
            manager_id = int(input("Enter the manager ID to edit: "))
            name = input("Enter new name (leave empty to keep current): ")
            phone_number = input("Enter new phone number (leave empty to keep current): ")
            email = input("Enter new email (leave empty to keep current): ")
            country = input("Enter new country (leave empty to keep current): ")
            hourly_rate = input("Enter new hourly rate (leave empty to keep current): ")
            amount_worked = input("Enter new amount worked (leave empty to keep current): ")

            # Collect only fields that are not empty
            new_values = {}
            if name:
                new_values['Name'] = name
            if phone_number:
                new_values['PhoneNumber'] = int(phone_number)
            if email:
                new_values['Email'] = email
            if country:
                new_values['Country'] = country
            if hourly_rate:
                new_values['HourlyRate'] = int(hourly_rate)
            if amount_worked:
                new_values['AmountWorked'] = int(amount_worked)

            if new_values:
                self.update_data(manager_id, new_values)
                print("Manager updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating manager: {e}")

    def delete_manager(self):
        """Delete a manager from the table."""
        try:
            manager_id = int(input("Enter the manager ID to delete: "))
            self.delete_data(manager_id)
            print("Manager deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting manager: {e}")

    def view_managers(self):
        """View all managers in the table."""
        try:
            managers = self.select_all()
            if managers:
                print("\nManagers in the table:")
                for manager in managers:
                    print(manager)
            else:
                print("No managers found.")
        except Exception as e:
            print(f"Error retrieving managers: {e}")

    def manage_managers(self):
        """Manage managers with a menu interface."""
        while True:
            print("\nManager Management")
            print("1. Add Manager")
            print("2. Edit Manager")
            print("3. Delete Manager")
            print("4. View All Managers")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_manager()
            elif choice == '2':
                self.edit_manager()
            elif choice == '3':
                self.delete_manager()
            elif choice == '4':
                self.view_managers()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
