import psycopg2
from src.db_engine import DBEngine
from src.Person import Person

class Worker(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, hourly_rate: float, amount_worked: int):
        super().__init__(name, phone, email, country)
        self.hourly_rate = hourly_rate
        self.amount_worked = amount_worked
        self.db_engine = DBEngine()  # Database engine instance

    def display_rate(self):
        print(f'Current hourly rate of {self.name} is {self.hourly_rate}')

    def display_amount_worked(self):
        print(f'{self.name} has worked {self.amount_worked} hours.')

    def display_salary(self):
        total = self.hourly_rate * self.amount_worked
        print(f'Current salary is: {total}')

    def save(self):
        """Save a new worker or update existing worker in the database."""
        if self.id is None:
            # New worker
            self._create_worker()
        else:
            # Existing worker
            self._update_worker()

    def _create_worker(self):
        """Insert a new worker into the database."""
        with self.db_engine.connection:
            with self.db_engine.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "Worker" ("Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "WorkerID"
                """, (self.name, self.phone, self.email, self.country, self.hourly_rate, self.amount_worked))
                self.id = cursor.fetchone()[0]
                self.db_engine.connection.commit()

    def _update_worker(self):
        """Update an existing worker's information."""
        with self.db_engine.connection:
            with self.db_engine.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE "Worker"
                    SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "HourlyRate" = %s, "AmountWorked" = %s
                    WHERE "WorkerID" = %s
                """, (self.name, self.phone, self.email, self.country, self.hourly_rate, self.amount_worked, self.id))
                self.db_engine.connection.commit()

    def delete(self):
        """Delete a worker from the database."""
        if self.id is not None:
            with self.db_engine.connection:
                with self.db_engine.connection.cursor() as cursor:
                    cursor.execute('DELETE FROM "Worker" WHERE "WorkerID" = %s', (self.id,))
                    self.db_engine.connection.commit()
                    self.id = None
        else:
            print("Worker ID is not set.")

    @classmethod
    def view_all(cls):
        """View all workers in the table."""
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM "Worker"')
                workers = cursor.fetchall()
                return workers

    def add_worker(self):
        """Add a new worker to the database."""
        try:
            name = input("Enter worker's name: ")
            phone_number = int(input("Enter worker's phone number: "))
            email = input("Enter worker's email: ")
            country = input("Enter worker's country: ")
            hourly_rate = float(input("Enter worker's hourly rate: "))
            amount_worked = int(input("Enter amount worked: "))

            new_worker = Worker(name, phone_number, email, country, hourly_rate, amount_worked)
            new_worker.save()
            print("Worker added successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding worker: {e}")

    def delete_worker(self):
        """Delete an existing worker by choosing from the list."""
        try:
            workers = self.view_all()
            if workers:
                print("Select a worker to delete:")
                for worker in workers:
                    print(
                        f"ID: {worker[0]}, Name: {worker[1]}, Phone: {worker[2]}, Email: {worker[3]}, Country: {worker[4]}, Hourly Rate: {worker[5]}, Amount Worked: {worker[6]}")

                worker_id = int(input("Enter the ID of the worker to delete: "))
                self.id = worker_id
                self.delete()
                print("Worker deleted successfully!")
            else:
                print("No workers found.")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting worker: {e}")

    def view_all_workers(self):
        """View all workers."""
        workers = self.view_all()
        if workers:
            print("All Workers:")
            for worker in workers:
                print(
                    f"ID: {worker[0]}, Name: {worker[1]}, Phone: {worker[2]}, Email: {worker[3]}, Country: {worker[4]}, Hourly Rate: {worker[5]}, Amount Worked: {worker[6]}")
        else:
            print("No workers found.")

    def display_all_salaries(self):
        """Display salaries of all workers."""
        workers = self.view_all()
        if workers:
            print("Salaries of All Workers:")
            for worker in workers:
                total = worker[5] * worker[6]  # HourlyRate * AmountWorked
                print(f"ID: {worker[0]}, Name: {worker[1]}, Salary: {total}")
        else:
            print("No workers found.")

    def display_all_rates(self):
        """Display hourly rates of all workers."""
        workers = self.view_all()
        if workers:
            print("Hourly Rates of All Workers:")
            for worker in workers:
                print(f"ID: {worker[0]}, Name: {worker[1]}, Hourly Rate: {worker[5]}")
        else:
            print("No workers found.")

    def display_all_amounts_worked(self):
        """Display amount worked of all workers."""
        workers = self.view_all()
        if workers:
            print("Amount Worked by All Workers:")
            for worker in workers:
                print(f"ID: {worker[0]}, Name: {worker[1]}, Amount Worked: {worker[6]}")
        else:
            print("No workers found.")


def main_menu():
    """Main menu to interact with worker functionalities."""
    while True:
        print("\nMain Menu")
        print("1. Manage Worker")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")

        if choice == '1':
            manage_worker_menu()
        elif choice == '2':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please select between 1 and 2.")


def manage_worker_menu():
    """Worker management menu with all options."""
    while True:
        print("\nWorker Management")
        print("1. Add Worker")
        print("2. Delete Worker")
        print("3. Display All Workers")
        print("4. Display All Salaries")
        print("5. Display All Hourly Rates")
        print("6. Display All Amounts Worked")
        print("7. Back")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            worker = Worker("", 0, "", "", 0.0, 0)  # Initialize without specific details
            worker.add_worker()
        elif choice == '2':
            worker = Worker("", 0, "", "", 0.0, 0)  # Initialize without specific details
            worker.delete_worker()
        elif choice == '3':
            worker = Worker("", 0, "", "", 0.0, 0)  # Initialize without specific details
            worker.view_all_workers()
        elif choice == '4':
            worker = Worker("", 0, "", "", 0.0, 0)  # Initialize without specific details
            worker.display_all_salaries()
        elif choice == '5':
            worker = Worker("", 0, "", "", 0.0, 0)  # Initialize without specific details
            worker.display_all_rates()
        elif choice == '6':
            worker = Worker("", 0, "", "", 0.0, 0)  # Initialize without specific details
            worker.display_all_amounts_worked()
        elif choice == '7':
            break
        else:
            print("Invalid choice, please select between 1 and 7.")


if __name__ == "__main__":
    main_menu()
