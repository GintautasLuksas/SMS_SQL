import os
import sys
import psycopg2
from psycopg2 import sql

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db_engine import DBEngine

class WorkerTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = '"Worker"'
        self.create_table()

    def create_table(self):
        """Create the Worker table if it doesn't exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS "Worker" (
            "WorkerID" SERIAL PRIMARY KEY,
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
        """Insert a new worker into the table."""
        insert_query = '''
        INSERT INTO "Worker" ("Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked")
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        self._execute_query(insert_query, data)

    def update_data(self, worker_id, new_values):
        """Update an existing worker's information."""
        set_clause = ', '.join([f'"{key}" = %s' for key in new_values.keys()])
        update_query = f'UPDATE "Worker" SET {set_clause} WHERE "WorkerID" = %s'
        values = list(new_values.values()) + [worker_id]
        self._execute_query(update_query, values)

    def delete_data(self, worker_id):
        """Delete a worker from the table."""
        delete_query = 'DELETE FROM "Worker" WHERE "WorkerID" = %s'
        self._execute_query(delete_query, (worker_id,))

    def select_all(self):
        """Select all workers from the table."""
        select_query = 'SELECT * FROM "Worker"'
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

    def add_worker(self):
        """Add a new worker to the table."""
        try:
            name = input("Enter worker's name: ")
            phone_number = int(input("Enter worker's phone number: "))
            email = input("Enter worker's email: ")
            country = input("Enter worker's country: ")
            hourly_rate = int(input("Enter worker's hourly rate: "))
            amount_worked = int(input("Enter amount worked: "))

            self.insert_data((name, phone_number, email, country, hourly_rate, amount_worked))
            print("Worker added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding worker: {e}")

    def edit_worker(self):
        """Edit an existing worker's information."""
        try:
            worker_id = int(input("Enter the worker ID to edit: "))
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
                self.update_data(worker_id, new_values)
                print("Worker updated successfully!")
            else:
                print("No changes were made.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error updating worker: {e}")

    def delete_worker(self):
        """Delete a worker from the table."""
        try:
            worker_id = int(input("Enter the worker ID to delete: "))
            self.delete_data(worker_id)
            print("Worker deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting worker: {e}")

    def view_workers(self):
        """View all workers in the table."""
        try:
            workers = self.select_all()
            if workers:
                print("\nWorkers in the table:")
                for worker in workers:
                    print(worker)
            else:
                print("No workers found.")
        except Exception as e:
            print(f"Error retrieving workers: {e}")

    def manage_workers(self):
        """Manage workers with a menu interface."""
        while True:
            print("\nWorker Management")
            print("1. Add Worker")
            print("2. Edit Worker")
            print("3. Delete Worker")
            print("4. View All Workers")
            print("5. Back")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_worker()
            elif choice == '2':
                self.edit_worker()
            elif choice == '3':
                self.delete_worker()
            elif choice == '4':
                self.view_workers()
            elif choice == '5':
                break
            else:
                print("Invalid choice, please select between 1 and 5.")
