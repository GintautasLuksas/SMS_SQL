from src.db_engine import DBEngine
from src.person.person import Person


class Manager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, monthly_salary: int, responsibility_id: int,
                 store_id: int, id: int = None):
        super().__init__(name, phone, email, country)
        self.monthly_salary = monthly_salary
        self.responsibility_id = responsibility_id
        self.store_id = store_id
        self.id = id  # Ensure ID is set if updating an existing manager

    def display_salary(self):
        print(f'{self.name}\'s monthly salary is: {self.monthly_salary}')

    def display_responsibility(self):
        print(f'{self.name} has responsibility ID: {self.responsibility_id}')

    def save(self):
        """Save a new manager or update an existing manager in the database."""
        if self.id is None:
            self._create_manager()
        else:
            self._update_manager()

    def _create_manager(self):
        """Insert a new manager into the database."""
        db = DBEngine()
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                INSERT INTO "Manager" ("Name", "PhoneNumber", "Email", "Country", "MonthlySalary", "ResponsibilityID", "StoreID")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "ManagerID"
            """, (self.name, self.phone, self.email, self.country, self.monthly_salary, self.responsibility_id,
                  self.store_id))
            self.id = cursor.fetchone()[0]
            db.connection.commit()
        except Exception as e:
            print(f"Error creating manager: {e}")
        finally:
            db.connection.close()

    def _update_manager(self):
        """Update an existing manager's information."""
        db = DBEngine()
        try:
            cursor = db.connection.cursor()
            cursor.execute("""
                UPDATE "Manager"
                SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "MonthlySalary" = %s, "ResponsibilityID" = %s, "StoreID" = %s
                WHERE "ManagerID" = %s
            """, (
            self.name, self.phone, self.email, self.country, self.monthly_salary, self.responsibility_id, self.store_id,
            self.id))
            db.connection.commit()
        except Exception as e:
            print(f"Error updating manager: {e}")
        finally:
            db.connection.close()

    def delete(self):
        """Delete a manager from the database."""
        if self.id is not None:
            db = DBEngine()
            try:
                cursor = db.connection.cursor()
                cursor.execute('DELETE FROM "Manager" WHERE "ManagerID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
            except Exception as e:
                print(f"Error deleting manager: {e}")
            finally:
                db.connection.close()
        else:
            print("Manager ID is not set.")

    @classmethod
    def view_all(cls):
        """View all managers in the table."""
        db = DBEngine()
        try:
            cursor = db.connection.cursor()
            cursor.execute('SELECT * FROM "Manager"')
            managers = cursor.fetchall()
            return managers
        except Exception as e:
            print(f"Error retrieving managers: {e}")
        finally:
            db.connection.close()

    @classmethod
    def display_all_salaries(cls):
        """Display all managers' salaries."""
        managers = cls.view_all()
        if managers:
            print("Salaries of All Managers:")
            for manager in managers:
                print(f"ID: {manager[0]}, Name: {manager[1]}, Salary: {manager[5]}")
        else:
            print("No managers found.")

    @classmethod
    def display_all_responsibilities(cls):
        """Display all managers' responsibility IDs."""
        managers = cls.view_all()
        if managers:
            print("Responsibilities of All Managers:")
            for manager in managers:
                print(f"ID: {manager[0]}, Name: {manager[1]}, Responsibility ID: {manager[6]}")
        else:
            print("No managers found.")

    @classmethod
    def manage_responsibilities(cls):
        """Manage responsibilities through a menu."""
        while True:
            print("\nResponsibility Management")
            print("1. Add Responsibility")
            print("2. Delete Responsibility")
            print("3. View All Responsibilities")
            print("4. Back")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                cls.add_responsibility()
            elif choice == '2':
                cls.delete_responsibility()
            elif choice == '3':
                cls.view_all_responsibilities()
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")

    @classmethod
    def add_responsibility(cls):
        """Add a new responsibility."""
        db = DBEngine()
        try:
            responsibility_name = input("Enter responsibility name: ")
            cursor = db.connection.cursor()
            cursor.execute("""
                INSERT INTO "Responsibilities" ("ResponsibilityName")
                VALUES (%s)
                RETURNING "ResponsibilityID"
            """, (responsibility_name,))
            responsibility_id = cursor.fetchone()[0]
            db.connection.commit()
            print(f"Responsibility added successfully with ID: {responsibility_id}")
        except Exception as e:
            print(f"Error adding responsibility: {e}")
        finally:
            db.connection.close()

    @classmethod
    def delete_responsibility(cls):
        """Delete a responsibility."""
        db = DBEngine()
        try:
            responsibility_id = int(input("Enter the ID of the responsibility to delete: "))
            cursor = db.connection.cursor()
            cursor.execute('DELETE FROM "Responsibilities" WHERE "ResponsibilityID" = %s', (responsibility_id,))
            db.connection.commit()
            print("Responsibility deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting responsibility: {e}")
        finally:
            db.connection.close()

    @classmethod
    def view_all_responsibilities(cls):
        """View all responsibilities."""
        db = DBEngine()
        try:
            cursor = db.connection.cursor()
            cursor.execute('SELECT * FROM "Responsibilities"')
            responsibilities = cursor.fetchall()
            if responsibilities:
                print("\nAll Responsibilities:")
                for responsibility in responsibilities:
                    print(f"ID: {responsibility[0]}, Name: {responsibility[1]}")
            else:
                print("No responsibilities found.")
        except Exception as e:
            print(f"Error retrieving responsibilities: {e}")
        finally:
            db.connection.close()


def manage_manager_menu():
    """Manager management menu with all options."""
    while True:
        print("\nManager Management")
        print("1. Add Manager")
        print("2. Edit Manager")
        print("3. Delete Manager")
        print("4. View All Managers")
        print("5. Display All Salaries")
        print("6. Display All Responsibility IDs")
        print("7. Manage Responsibilities")
        print("8. Back")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            add_manager()
        elif choice == '2':
            edit_manager()
        elif choice == '3':
            delete_manager()
        elif choice == '4':
            view_all_managers()
        elif choice == '5':
            display_all_salaries()
        elif choice == '6':
            display_all_responsibilities()
        elif choice == '7':
            Manager.manage_responsibilities()
        elif choice == '8':
            break
        else:
            print("Invalid choice, please select between 1 and 8.")


def add_manager():
    """Add a new manager."""
    name = input("Enter manager's name: ")
    phone = int(input("Enter manager's phone number: "))
    email = input("Enter manager's email: ")
    country = input("Enter manager's country: ")
    monthly_salary = int(input("Enter manager's monthly salary: "))
    responsibility_id = int(input("Enter manager's responsibility ID: "))
    store_id = int(input("Enter manager's store ID: "))

    manager = Manager(name, phone, email, country, monthly_salary, responsibility_id, store_id)
    manager.save()
    print("Manager added successfully.")


def edit_manager():
    """Edit an existing manager."""
    manager_id = int(input("Enter the ID of the manager to edit: "))
    db = DBEngine()
    try:
        cursor = db.connection.cursor()
        cursor.execute('SELECT * FROM "Manager" WHERE "ManagerID" = %s', (manager_id,))
        manager = cursor.fetchone()

        if manager:
            print(
                f"Current details: Name: {manager[1]}, Phone: {manager[2]}, Email: {manager[3]}, Country: {manager[4]}, Monthly Salary: {manager[5]}, Responsibility ID: {manager[6]}, Store ID: {manager[7]}")

            name = input("Enter new manager's name (leave empty to keep current): ") or manager[1]
            phone = input("Enter new manager's phone number (leave empty to keep current): ") or manager[2]
            email = input("Enter new manager's email (leave empty to keep current): ") or manager[3]
            country = input("Enter new manager's country (leave empty to keep current): ") or manager[4]
            monthly_salary = input("Enter new manager's monthly salary (leave empty to keep current): ")
            monthly_salary = int(monthly_salary) if monthly_salary else manager[5]
            responsibility_id = input("Enter new manager's responsibility ID (leave empty to keep current): ")
            responsibility_id = int(responsibility_id) if responsibility_id else manager[6]
            store_id = input("Enter new manager's store ID (leave empty to keep current): ")
            store_id = int(store_id) if store_id else manager[7]

            cursor.execute("""
                UPDATE "Manager"
                SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "MonthlySalary" = %s, "ResponsibilityID" = %s, "StoreID" = %s
                WHERE "ManagerID" = %s
            """, (name, phone, email, country, monthly_salary, responsibility_id, store_id, manager_id))
            db.connection.commit()
            print("Manager details updated successfully.")
        else:
            print("Manager not found.")
    except Exception as e:
        print(f"Error editing manager: {e}")
    finally:
        db.connection.close()


def delete_manager():
    """Delete an existing manager."""
    manager_id = int(input("Enter the ID of the manager to delete: "))
    manager = Manager(id=manager_id)
    manager.delete()
    print("Manager deleted successfully.")


def view_all_managers():
    """View all managers with all available details."""
    managers = Manager.view_all()
    if managers:
        print("\nAll Managers:")
        for manager in managers:
            print(f"ID: {manager[0]}")
            print(f"Name: {manager[1]}")
            print(f"Phone Number: {manager[2]}")
            print(f"Email: {manager[3]}")
            print(f"Country: {manager[4]}")
            print(f"Monthly Salary: {manager[5]}")
            print(f"Responsibility ID: {manager[6]}")
            print(f"Store ID: {manager[7]}")
            print("-" * 40)  # Separator for better readability
    else:
        print("No managers found.")


def display_all_salaries():
    """Display all managers' salaries."""
    Manager.display_all_salaries()


def display_all_responsibilities():
    """Display all managers' responsibility IDs."""
    Manager.display_all_responsibilities()


manage_manager_menu()
