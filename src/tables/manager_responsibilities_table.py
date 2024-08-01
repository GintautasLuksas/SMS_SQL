import os
import sys
import psycopg2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db_engine import DBEngine

class ManagerResponsibilitiesTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Manager Responsibilities"'
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Manager Responsibilities" (
            "MGRResponsibilityID" INT NOT NULL,
            "ResponsibilityID" INT NOT NULL,
            "ManagerID" INT NOT NULL,
            PRIMARY KEY ("MGRResponsibilityID")
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "Manager Responsibilities" ("MGRResponsibilityID", "ResponsibilityID", "ManagerID")
        VALUES (%s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def delete_data(self, mgr_responsibility_id):
        delete_query = 'DELETE FROM "Manager Responsibilities" WHERE "MGRResponsibilityID" = %s'
        self._execute_query(delete_query, (mgr_responsibility_id,))

    def select_all(self):
        select_query = 'SELECT * FROM "Manager Responsibilities"'
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

    def add_mgr_responsibility(self):
        try:
            mgr_responsibility_id = int(input("Enter manager responsibility ID: "))
            responsibility_id = int(input("Enter responsibility ID: "))
            manager_id = int(input("Enter manager ID: "))

            self.insert_data((mgr_responsibility_id, responsibility_id, manager_id))
            print("Manager responsibility added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding manager responsibility: {e}")

    def delete_mgr_responsibility(self):
        try:
            mgr_responsibility_id = int(input("Enter the manager responsibility ID to delete: "))
            self.delete_data(mgr_responsibility_id)
            print("Manager responsibility deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting manager responsibility: {e}")

    def view_mgr_responsibilities(self):
        try:
            responsibilities = self.select_all()
            if responsibilities:
                print("\nManager Responsibilities:")
                for responsibility in responsibilities:
                    print(responsibility)
            else:
                print("No manager responsibilities found.")
        except Exception as e:
            print(f"Error retrieving manager responsibilities: {e}")

    def manage_manager_responsibilities(self):
        while True:
            print("\nManager Responsibilities Management")
            print("1. Add Manager Responsibility")
            print("2. Delete Manager Responsibility")
            print("3. View All Manager Responsibilities")
            print("4. Back")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_mgr_responsibility()
            elif choice == '2':
                self.delete_mgr_responsibility()
            elif choice == '3':
                self.view_mgr_responsibilities()
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")
