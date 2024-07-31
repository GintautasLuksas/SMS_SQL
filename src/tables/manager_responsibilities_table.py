import os
import sys
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class ManagerResponsibilitiesTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"ManagerResponsibilities"'

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "ManagerResponsibilities" (
            "ResponsibilityID" SERIAL PRIMARY KEY,
            "ManagerID" INT NOT NULL,
            "ResponsibilityDescription" TEXT NOT NULL,
            FOREIGN KEY ("ManagerID") REFERENCES "Manager" ("ManagerID")
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "ManagerResponsibilities" ("ManagerID", "ResponsibilityDescription")
        VALUES (%s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, responsibility_id, new_values):
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "ManagerResponsibilities" SET {set_clause} WHERE "ResponsibilityID" = %s'
        values = list(new_values.values()) + [responsibility_id]
        self._execute_query(update_query, values)

    def delete_data(self, responsibility_id):
        delete_query = 'DELETE FROM "ManagerResponsibilities" WHERE "ResponsibilityID" = %s'
        self._execute_query(delete_query, (responsibility_id,))

    def select_all(self):
        select_query = 'SELECT * FROM "ManagerResponsibilities"'
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

    def add_responsibility(self):
        try:
            manager_id = int(input("Enter manager ID: "))
            description = input("Enter responsibility description: ")

            self.insert_data((manager_id, description))
            print("Responsibility added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding responsibility: {e}")

    def edit_responsibility(self):
        try:
            responsibility_id = int(input("Enter the Responsibility ID to edit: "))
            manager_id = input("Enter new manager ID (leave empty to keep current): ")
            description = input("Enter new responsibility description (leave empty to keep current): ")

            new_values = {}
            if manager_id:
                new_values['ManagerID'] = int(manager_id)
            if description:
                new_values['ResponsibilityDescription'] = description

            if new_values:
                self.update_data(responsibility_id, new_values)
                print("Responsibility updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating responsibility: {e}")

    def delete_responsibility(self):
        try:
            responsibility_id = int(input("Enter the Responsibility ID to delete: "))
            self.delete_data(responsibility_id)
            print("Responsibility deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting responsibility: {e}")

    def view_responsibilities(self):
        try:
            responsibilities = self.select_all()
            if responsibilities:
                print("\nResponsibilities in the table:")
                for responsibility in responsibilities:
                    print(responsibility)
            else:
                print("No responsibilities found.")
        except Exception as e:
            print(f"Error retrieving responsibilities: {e}")

    def manage_responsibilities(self):
        while True:
            print("\nResponsibilities Management")
            print("1. Add Responsibility")
            print("2. Edit Responsibility")
            print("3. Delete Responsibility")
            print("4. View All Responsibilities")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_responsibility()
            elif choice == '2':
                self.edit_responsibility()
            elif choice == '3':
                self.delete_responsibility()
            elif choice == '4':
                self.view_responsibilities()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
