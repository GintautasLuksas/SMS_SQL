from typing import Optional
from src.db_engine import DBEngine
from src.person.person import Person

class Worker(Person):
    """This is Worker class which is added through Person class."""
    def __init__(self, name: str, phone: int, email: str, country: str,
                 hourly_rate: int, amount_worked: int, store_id: int, id: Optional[int] = None) -> None:
        super().__init__(name, phone, email, country, id)
        self.hourly_rate = hourly_rate
        self.amount_worked = amount_worked
        self.store_id = store_id

    def display_salary(self) -> None:
        """Display the salary of the worker.

        Calculate and print the salary based on hourly rate and amount worked.
        """
        salary = self.hourly_rate * self.amount_worked
        print(f'{self.name}\'s salary is: {salary}')

    def save(self) -> None:
        """Save or update the worker in the database.

        If the worker does not have an ID, create a new worker record. Otherwise,
        update the existing worker record.
        """
        if self.id is None:
            self._create_worker()
        else:
            self._update_worker()

    def _create_worker(self) -> None:
        """Create a new worker record in the database.

        Insert a new worker record and set the worker's ID based on the database's
        auto-generated ID.
        """
        db = DBEngine()
        if db.cursor is None or db.connection is None:
            print("Database connection not established.")
            return

        try:
            db.cursor.execute("""
                INSERT INTO "Worker" ("Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked", "StoreID")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "WorkerID"
            """, (self.name, self.phone, self.email, self.country, self.hourly_rate, self.amount_worked, self.store_id))
            self.id = db.cursor.fetchone()[0]
            db.connection.commit()
            print("Worker created successfully.")
        except Exception as e:
            print(f"Error creating worker: {e}")
        finally:
            if db.cursor:
                db.cursor.close()
            if db.connection:
                db.connection.close()

    def _update_worker(self) -> None:
        """Update an existing worker record in the database.

        Modify the details of an existing worker record based on the worker's ID.
        """
        db = DBEngine()
        if db.cursor is None or db.connection is None:
            print("Database connection not established.")
            return

        try:
            db.cursor.execute("""
                UPDATE "Worker"
                SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "HourlyRate" = %s, "AmountWorked" = %s, "StoreID" = %s
                WHERE "WorkerID" = %s
            """, (self.name, self.phone, self.email, self.country, self.hourly_rate, self.amount_worked, self.store_id,
                  self.id))
            db.connection.commit()
            print("Worker updated successfully.")
        except Exception as e:
            print(f"Error updating worker: {e}")
        finally:
            if db.cursor:
                db.cursor.close()
            if db.connection:
                db.connection.close()

    def delete(self) -> None:
        """Delete the worker record from the database.

        Remove the worker record from the database based on the worker's ID.
        """
        if self.id is not None:
            db = DBEngine()
            if db.cursor is None or db.connection is None:
                print("Database connection not established.")
                return

            try:
                db.cursor.execute('DELETE FROM "Worker" WHERE "WorkerID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
                print("Worker deleted successfully.")
            except Exception as e:
                print(f"Error deleting worker: {e}")
            finally:
                if db.cursor:
                    db.cursor.close()
                if db.connection:
                    db.connection.close()
        else:
            print("Worker ID is not set.")

    @classmethod
    def view_all(cls) -> None:
        """View all workers in the database and print them.

        Fetch all worker records from the database and print them. If no workers
        are found, print a corresponding message.
        """
        db = DBEngine()
        if db.cursor is None or db.connection is None:
            print("Database connection not established.")
            return

        try:
            db.cursor.execute("""
                SELECT "WorkerID", "Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked", "StoreID"
                FROM "Worker"
            """)
            workers = db.cursor.fetchall()
            if workers:
                print("List of Workers:")
                for worker in workers:
                    print(f"ID: {worker[0]}, Name: {worker[1]}, Phone: {worker[2]}, Email: {worker[3]}, Country: {worker[4]}, "
                          f"Hourly Rate: {worker[5]}, Amount Worked: {worker[6]}, Store ID: {worker[7]}")
            else:
                print("No workers found.")
        except Exception as e:
            print(f"Error retrieving workers: {e}")
        finally:
            if db.cursor:
                db.cursor.close()
            if db.connection:
                db.connection.close()

    @classmethod
    def display_all_salaries(cls) -> None:
        """Display salaries of all workers.

        Retrieve all workers and print their salaries based on hourly rate and amount
        worked. This method assumes `view_all` prints workers as well.
        """
        workers = cls.view_all()
        if workers:
            print("Salaries of All Workers:")
            for w in workers:
                salary = w[5] * w[6]
                print(f"ID: {w[0]}, Name: {w[1]}, Salary: {salary}")
        else:
            print("No workers found.")

    @classmethod
    def manage_workers(cls) -> None:
        """Display the worker management menu and handle user input.

        Provide a menu for managing workers, including adding, editing, deleting,
        viewing, and displaying salaries. The loop continues until the user chooses
        to exit.
        """
        while True:
            print("\nWorker Management Menu")
            print("1. Add Worker")
            print("2. Edit Worker")
            print("3. Delete Worker")
            print("4. View All Workers")
            print("5. Display All Salaries")
            print("6. Back")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                cls.add_worker()
            elif choice == '2':
                cls.edit_worker()
            elif choice == '3':
                cls.delete_worker()
            elif choice == '4':
                cls.view_all_workers()
            elif choice == '5':
                cls.display_all_salaries()
            elif choice == '6':
                break
            else:
                print("Invalid choice, please select between 1 and 6.")

    @classmethod
    def add_worker(cls) -> None:
        """Add a new worker based on user input.

        Prompt the user for worker details and create a new worker. Handle input
        validation and potential errors.
        """
        try:
            name = input("Enter worker's name: ").strip()
            phone = int(input("Enter worker's phone number: ").strip())
            email = input("Enter worker's email: ").strip()
            country = input("Enter worker's country: ").strip()
            hourly_rate = int(input("Enter worker's hourly rate: ").strip())
            amount_worked = int(input("Enter amount worked: ").strip())
            store_id = int(input("Enter store ID: ").strip())

            worker = cls(name, phone, email, country, hourly_rate, amount_worked, store_id)
            worker.save()
            print("Worker added successfully.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")

    @classmethod
    def edit_worker(cls) -> None:
        """Edit an existing worker based on user input.

        Allow the user to modify details of an existing worker by providing the worker's
        ID. Update the worker's information in the database.
        """
        try:
            worker_id = int(input("Enter the ID of the worker to edit: ").strip())

            db = DBEngine()
            if db.cursor is None or db.connection is None:
                print("Database connection not established.")
                return

            db.cursor.execute("""
                SELECT "WorkerID", "Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked", "StoreID"
                FROM "Worker"
                WHERE "WorkerID" = %s
            """, (worker_id,))
            worker_data = db.cursor.fetchone()

            if worker_data:
                name = input(f"Enter new name (current: {worker_data[1]}): ").strip() or worker_data[1]
                phone_input = input(f"Enter new phone number (current: {worker_data[2]}): ").strip()
                phone = int(phone_input) if phone_input else worker_data[2]
                email = input(f"Enter new email (current: {worker_data[3]}): ").strip() or worker_data[3]
                country = input(f"Enter new country (current: {worker_data[4]}): ").strip() or worker_data[4]
                hourly_rate_input = input(f"Enter new hourly rate (current: {worker_data[5]}): ").strip()
                hourly_rate = int(hourly_rate_input) if hourly_rate_input else worker_data[5]
                amount_worked_input = input(f"Enter new amount worked (current: {worker_data[6]}): ").strip()
                amount_worked = int(amount_worked_input) if amount_worked_input else worker_data[6]
                store_id_input = input(f"Enter new store ID (current: {worker_data[7]}): ").strip()
                store_id = int(store_id_input) if store_id_input else worker_data[7]

                worker = cls(name, phone, email, country, hourly_rate, amount_worked, store_id, worker_id)
                worker.save()
                print("Worker updated successfully.")
            else:
                print("Worker not found.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")

    @classmethod
    def delete_worker(cls) -> None:
        """Delete a worker based on user input.

        Prompt the user for the worker's ID and delete the corresponding worker
        from the database.
        """
        try:
            worker_id = int(input("Enter the ID of the worker to delete: ").strip())
            worker = cls('', 0, '', '', 0, 0, 0, worker_id)
            worker.delete()
            print("Worker deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")

    @classmethod
    def view_all_workers(cls) -> None:
        """View all workers by calling the `view_all` method.

        Fetch and print all worker records by invoking the `view_all` method.
        """
        cls.view_all()
