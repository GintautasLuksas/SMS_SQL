import os
import sys
import psycopg2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db_engine import DBEngine
class SMResponsibilitiesTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"SM Responsibilities"'
        self.create_table()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "SM Responsibilities" (
            "SMResponsibilityID" INT NOT NULL,
            "ResponsibilityID" INT NOT NULL,
            "StoreManagerID" INT NOT NULL,
            PRIMARY KEY ("SMResponsibilityID")
        );
        '''
        self._execute_query(create_table_query)

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO "SM Responsibilities" ("SMResponsibilityID", "ResponsibilityID", "StoreManagerID")
        VALUES (%s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def delete_data(self, sm_responsibility_id):
        delete_query = 'DELETE FROM "SM Responsibilities" WHERE "SMResponsibilityID" = %s'
        self._execute_query(delete_query, (sm_responsibility_id,))

    def select_all(self):
        select_query = 'SELECT * FROM "SM Responsibilities"'
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

    def add_sm_responsibility(self):
        try:
            sm_responsibility_id = int(input("Enter store manager responsibility ID: "))
            responsibility_id = int(input("Enter responsibility ID: "))
            store_manager_id = int(input("Enter store manager ID: "))

            self.insert_data((sm_responsibility_id, responsibility_id, store_manager_id))
            print("Store manager responsibility added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding store manager responsibility: {e}")

    def delete_sm_responsibility(self):
        try:
            sm_responsibility_id = int(input("Enter the store manager responsibility ID to delete: "))
            self.delete_data(sm_responsibility_id)
            print("Store manager responsibility deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting store manager responsibility: {e}")

    def view_sm_responsibilities(self):
        try:
            responsibilities = self.select_all()
            if responsibilities:
                print("\nStore Manager Responsibilities:")
                for responsibility in responsibilities:
                    print(responsibility)
            else:
                print("No store manager responsibilities found.")
        except Exception as e:
            print(f"Error retrieving store manager responsibilities: {e}")

    def manage_sm_responsibilities(self):
        while True:
            print("\nStore Manager Responsibilities Management")
            print("1. Add Store Manager Responsibility")
            print("2. Delete Store Manager Responsibility")
            print("3. View All Store Manager Responsibilities")
            print("4. Back")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_sm_responsibility()
            elif choice == '2':
                self.delete_sm_responsibility()
            elif choice == '3':
                self.view_sm_responsibilities()
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")
