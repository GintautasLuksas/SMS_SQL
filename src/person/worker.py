from src.db_engine import DBEngine
from src.person.person import Person

class Worker(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, hourly_rate: int, amount_worked: int, store_id: int, id: int = None):
        super().__init__(name, phone, email, country)
        self.hourly_rate = hourly_rate
        self.amount_worked = amount_worked
        self.store_id = store_id
        self.id = id

    def display_salary(self):
        """Display the worker's salary based on hourly rate and amount worked."""
        salary = self.hourly_rate * self.amount_worked
        print(f'{self.name}\'s salary is: {salary}')

    def save(self):
        """Save a new worker or update an existing worker in the database."""
        if self.id is None:
            self._create_worker()
        else:
            self._update_worker()

    def _create_worker(self):
        """Insert a new worker into the database."""
        db = DBEngine()
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
            db.cursor.close()
            db.connection.close()

    def _update_worker(self):
        """Update an existing worker's information."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                UPDATE "Worker"
                SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "HourlyRate" = %s, "AmountWorked" = %s, "StoreID" = %s
                WHERE "WorkerID" = %s
            """, (self.name, self.phone, self.email, self.country, self.hourly_rate, self.amount_worked, self.store_id, self.id))
            db.connection.commit()
            print("Worker updated successfully.")
        except Exception as e:
            print(f"Error updating worker: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    def delete(self):
        """Delete a worker from the database."""
        if self.id is not None:
            db = DBEngine()
            try:
                db.cursor.execute('DELETE FROM "Worker" WHERE "WorkerID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
                print("Worker deleted successfully.")
            except Exception as e:
                print(f"Error deleting worker: {e}")
            finally:
                db.cursor.close()
                db.connection.close()
        else:
            print("Worker ID is not set.")

    @classmethod
    def view_all(cls):
        """View all workers in the table."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                SELECT "WorkerID", "Name", "PhoneNumber", "Email", "Country", "HourlyRate", "AmountWorked", "StoreID"
                FROM "Worker"
            """)
            workers = db.cursor.fetchall()
            return workers
        except Exception as e:
            print(f"Error retrieving workers: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def display_all_salaries(cls):
        """Display all workers' salaries."""
        workers = cls.view_all()
        if workers:
            print("Salaries of All Workers:")
            for w in workers:
                salary = w[5] * w[6]  # HourlyRate * AmountWorked
                print(f"ID: {w[0]}, Name: {w[1]}, Salary: {salary}")
        else:
            print("No workers found.")

    @classmethod
    def manage_workers(cls):
        """Manage workers through a menu."""
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
    def add_worker(cls):
        """Add a new worker."""
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
    def edit_worker(cls):
        """Edit an existing worker."""
        try:
            worker_id = int(input("Enter the ID of the worker to edit: ").strip())
            db = DBEngine()
            db.cursor.execute('SELECT * FROM "Worker" WHERE "WorkerID" = %s', (worker_id,))
            worker_data = db.cursor.fetchone()
            if worker_data:
                name = input(f"Enter new name (current: {worker_data[1]}): ").strip() or worker_data[1]
                phone = input(f"Enter new phone number (current: {worker_data[2]}): ").strip()
                phone = int(phone) if phone else worker_data[2]
                email = input(f"Enter new email (current: {worker_data[3]}): ").strip() or worker_data[3]
                country = input(f"Enter new country (current: {worker_data[4]}): ").strip() or worker_data[4]
                hourly_rate = input(f"Enter new hourly rate (current: {worker_data[5]}): ").strip()
                hourly_rate = int(hourly_rate) if hourly_rate else worker_data[5]
                amount_worked = input(f"Enter new amount worked (current: {worker_data[6]}): ").strip()
                amount_worked = int(amount_worked) if amount_worked else worker_data[6]
                store_id = input(f"Enter new store ID (current: {worker_data[7]}): ").strip()
                store_id = int(store_id) if store_id else worker_data[7]

                worker = cls(name, phone, email, country, hourly_rate, amount_worked, store_id, worker_id)
                worker.save()
                print("Worker updated successfully.")
            else:
                print("Worker not found.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")
        except Exception as e:
            print(f"Error editing worker: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def delete_worker(cls):
        """Delete an existing worker."""
        try:
            worker_id = int(input("Enter the ID of the worker to delete: ").strip())
            worker = cls(name='', phone=0, email='', country='', hourly_rate=0, amount_worked=0, store_id=0, id=worker_id)
            worker.delete()
            print("Worker deleted successfully.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    @classmethod
    def view_all_workers(cls):
        """View all workers."""
        workers = cls.view_all()
        if workers:
            for worker in workers:
                salary = worker[5] * worker[6]  # HourlyRate * AmountWorked
                print(f"ID: {worker[0]}, Name: {worker[1]}, Hourly Rate: {worker[5]}, Amount Worked: {worker[6]}, Salary: {salary}")
        else:
            print("No workers found.")

    @classmethod
    def display_all_salaries(cls):
        """Display all workers' salaries."""
        cls.display_all_salaries()
