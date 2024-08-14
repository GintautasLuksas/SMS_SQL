from src.db_engine import DBEngine
from src.Person import Person

class StoreManager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, store_id: int, sm_responsibility_id: int,
                 monthly_salary: int, petty_cash: int, id: int = None):
        super().__init__(name, phone, email, country)
        self.store_id = store_id
        self.sm_responsibility_id = sm_responsibility_id
        self.monthly_salary = monthly_salary
        self.petty_cash = petty_cash
        self.id = id

    def display_salary(self):
        print(f'{self.name}\'s monthly salary is: {self.monthly_salary}')

    def display_responsibility(self):
        print(f'{self.name} has responsibility ID: {self.sm_responsibility_id}')

    def save(self):
        """Save a new store manager or update an existing store manager in the database."""
        if self.id is None:
            self._create_store_manager()
        else:
            self._update_store_manager()

    def _create_store_manager(self):
        """Insert a new store manager into the database."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute("""
                INSERT INTO "Store Manager" ("Name", "Country", "Email", "PhoneNumber", "StoreID", "SMResponsibilityID", "MonthlySalary", "PettyCash")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "StoreManagerID"
            """, (self.name, self.country, self.email, self.phone, self.store_id, self.sm_responsibility_id, self.monthly_salary, self.petty_cash))
            self.id = cursor.fetchone()[0]
            connection.commit()
        except Exception as e:
            print(f"Error creating store manager: {e}")
        finally:
            cursor.close()
            connection.close()

    def _update_store_manager(self):
        """Update an existing store manager's information."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute("""
                UPDATE "Store Manager"
                SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "StoreID" = %s, "SMResponsibilityID" = %s, "MonthlySalary" = %s, "PettyCash" = %s
                WHERE "StoreManagerID" = %s
            """, (self.name, self.phone, self.email, self.country, self.store_id, self.sm_responsibility_id, self.monthly_salary, self.petty_cash, self.id))
            connection.commit()
        except Exception as e:
            print(f"Error updating store manager: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete(self):
        """Delete a store manager from the database."""
        if self.id is not None:
            db = DBEngine()
            connection = db.connection
            cursor = db.cursor
            try:
                cursor.execute('DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s', (self.id,))
                connection.commit()
                self.id = None
            except Exception as e:
                print(f"Error deleting store manager: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            print("Store Manager ID is not set.")

    @classmethod
    def view_all(cls):
        """View all store managers in the table."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute('SELECT * FROM "Store Manager"')
            store_managers = cursor.fetchall()
            return store_managers
        except Exception as e:
            print(f"Error retrieving store managers: {e}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def display_all_salaries(cls):
        """Display all store managers' salaries."""
        store_managers = cls.view_all()
        if store_managers:
            print("Salaries of All Store Managers:")
            for sm in store_managers:
                print(f"ID: {sm[0]}, Name: {sm[2]}, Salary: {sm[6]}")
        else:
            print("No store managers found.")

    @classmethod
    def display_all_responsibilities(cls):
        """Display all store managers' responsibility IDs."""
        store_managers = cls.view_all()
        if store_managers:
            print("Responsibilities of All Store Managers:")
            for sm in store_managers:
                print(f"ID: {sm[0]}, Name: {sm[2]}, Responsibility ID: {sm[5]}")
        else:
            print("No store managers found.")

    @classmethod
    def manage_responsibilities(cls):
        """Manage store manager responsibilities through a menu."""
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
        connection = db.connection
        cursor = db.cursor
        try:
            responsibility_name = input("Enter responsibility name: ")
            cursor.execute("""
                INSERT INTO "SM Responsibilities" ("ResponsibilityName")
                VALUES (%s)
                RETURNING "SMResponsibilityID"
            """, (responsibility_name,))
            responsibility_id = cursor.fetchone()[0]
            connection.commit()
            print(f"Responsibility added successfully with ID: {responsibility_id}")
        except Exception as e:
            print(f"Error adding responsibility: {e}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete_responsibility(cls):
        """Delete a responsibility."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            responsibility_id = int(input("Enter the ID of the responsibility to delete: "))
            cursor.execute('DELETE FROM "SM Responsibilities" WHERE "SMResponsibilityID" = %s', (responsibility_id,))
            connection.commit()
            print("Responsibility deleted successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error deleting responsibility: {e}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def view_all_responsibilities(cls):
        """View all responsibilities."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute('SELECT * FROM "SM Responsibilities"')
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
            cursor.close()
            connection.close()

def manage_store_manager_menu():
    """Store Manager management menu with all options."""
    while True:
        print("\nStore Manager Management")
        print("1. Add Store Manager")
        print("2. Edit Store Manager")
        print("3. Delete Store Manager")
        print("4. View All Store Managers")
        print("5. Display All Salaries")
        print("6. Display All Responsibility IDs")
        print("7. Manage Responsibilities")
        print("8. Back")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            add_store_manager()
        elif choice == '2':
            edit_store_manager()
        elif choice == '3':
            delete_store_manager()
        elif choice == '4':
            view_all_store_managers()
        elif choice == '5':
            display_all_salaries()
        elif choice == '6':
            display_all_responsibilities()
        elif choice == '7':
            StoreManager.manage_responsibilities()
        elif choice == '8':
            break
        else:
            print("Invalid choice, please select between 1 and 8.")

def add_store_manager():
    """Add a new store manager."""
    name = input("Enter store manager's name: ")
    phone = int(input("Enter store manager's phone number: "))
    email = input("Enter store manager's email: ")
    country = input("Enter store manager's country: ")
    store_id = int(input("Enter store ID: "))
    sm_responsibility_id = int(input("Enter responsibility ID: "))
    monthly_salary = int(input("Enter store manager's monthly salary: "))
    petty_cash = int(input("Enter store manager's petty cash: "))

    store_manager = StoreManager(name, phone, email, country, store_id, sm_responsibility_id, monthly_salary, petty_cash)
    store_manager.save()
    print("Store Manager added successfully.")

def edit_store_manager():
    """Edit an existing store manager."""
    manager_id = int(input("Enter the ID of the store manager to edit: "))
    db = DBEngine()
    connection = db.connection
    cursor = db.cursor
    try:
        cursor.execute('SELECT * FROM "Store Manager" WHERE "StoreManagerID" = %s', (manager_id,))
        manager_data = cursor.fetchone()
        if manager_data:
            name = input(f"Enter new name (current: {manager_data[2]}): ") or manager_data[2]
            phone = int(input(f"Enter new phone number (current: {manager_data[5]}): ") or manager_data[5])
            email = input(f"Enter new email (current: {manager_data[4]}): ") or manager_data[4]
            country = input(f"Enter new country (current: {manager_data[3]}): ") or manager_data[3]
            store_id = int(input(f"Enter new store ID (current: {manager_data[1]}): ") or manager_data[1])
            sm_responsibility_id = int(input(f"Enter new responsibility ID (current: {manager_data[6]}): ") or manager_data[6])
            monthly_salary = int(input(f"Enter new monthly salary (current: {manager_data[7]}): ") or manager_data[7])
            petty_cash = int(input(f"Enter new petty cash (current: {manager_data[8]}): ") or manager_data[8])

            store_manager = StoreManager(name, phone, email, country, store_id, sm_responsibility_id, monthly_salary, petty_cash, manager_id)
            store_manager.save()
            print("Store Manager updated successfully.")
        else:
            print("Store Manager not found.")
    except Exception as e:
        print(f"Error editing store manager: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_store_manager():
    """Delete a store manager."""
    manager_id = int(input("Enter the ID of the store manager to delete: "))
    db = DBEngine()
    connection = db.connection
    cursor = db.cursor
    try:
        cursor.execute('SELECT * FROM "Store Manager" WHERE "StoreManagerID" = %s', (manager_id,))
        manager_data = cursor.fetchone()
        if manager_data:
            store_manager = StoreManager(name=manager_data[2], phone=manager_data[5], email=manager_data[4], country=manager_data[3],
                                         store_id=manager_data[1], sm_responsibility_id=manager_data[6], monthly_salary=manager_data[7], petty_cash=manager_data[8], id=manager_id)
            store_manager.delete()
            print("Store Manager deleted successfully.")
        else:
            print("Store Manager not found.")
    except Exception as e:
        print(f"Error deleting store manager: {e}")
    finally:
        cursor.close()
        connection.close()

def view_all_store_managers():
    """View all store managers."""
    store_managers = StoreManager.view_all()
    if store_managers:
        print("\nAll Store Managers:")
        for sm in store_managers:
            print(f"ID: {sm[0]}, Store ID: {sm[1]}, Name: {sm[2]}, Country: {sm[3]}, Email: {sm[4]}, Phone: {sm[5]}, Monthly Salary: {sm[6]}, Petty Cash: {sm[7]}, Responsibility ID: {sm[8]}")
    else:
        print("No store managers found.")

def display_all_salaries():
    """Display all store managers' salaries."""
    StoreManager.display_all_salaries()

def display_all_responsibilities():
    """Display all store managers' responsibility IDs."""
    StoreManager.display_all_responsibilities()

# Main program entry point
if __name__ == "__main__":
    manage_store_manager_menu()
