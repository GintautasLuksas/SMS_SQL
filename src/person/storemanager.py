from src.db_engine import DBEngine
from src.person.person import Person

class StoreManager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, store_id: int,
                 monthly_salary: int, petty_cash: int, id: int = None):
        super().__init__(name, phone, email, country)
        self.store_id = store_id
        self.monthly_salary = monthly_salary
        self.petty_cash = petty_cash
        self.id = id

    def display_salary(self):
        """Display the store manager's monthly salary."""
        print(f"{self.name}'s monthly salary is: {self.monthly_salary}")

    def save(self):
        """Save a new store manager or update an existing store manager in the database."""
        if self.id is None:
            self._create_store_manager()
        else:
            self._update_store_manager()

    def _create_store_manager(self):
        """Insert a new store manager into the database."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                INSERT INTO "Store Manager" ("StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "StoreManagerID"
            """, (self.store_id, self.name, self.country, self.email, self.phone, self.monthly_salary, self.petty_cash))
            self.id = db.cursor.fetchone()[0]
            db.connection.commit()
            print("Store Manager created successfully.")
        except Exception as e:
            print(f"Error creating store manager: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    def _update_store_manager(self):
        """Update an existing store manager's information."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                UPDATE "Store Manager"
                SET "StoreID" = %s, "Name" = %s, "Country" = %s, "Email" = %s, "PhoneNumber" = %s, "MonthlySalary" = %s, "PettyCash" = %s
                WHERE "StoreManagerID" = %s
            """, (self.store_id, self.name, self.country, self.email, self.phone, self.monthly_salary, self.petty_cash, self.id))
            db.connection.commit()
            print("Store Manager updated successfully.")
        except Exception as e:
            print(f"Error updating store manager: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    def delete(self):
        """Delete a store manager from the database."""
        if self.id is not None:
            db = DBEngine()
            try:
                db.cursor.execute('DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
                print("Store Manager deleted successfully.")
            except Exception as e:
                print(f"Error deleting store manager: {e}")
            finally:
                db.cursor.close()
                db.connection.close()
        else:
            print("Store Manager ID is not set.")

    @classmethod
    def view_all(cls):
        """View all store managers in the table."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                SELECT "StoreManagerID", "StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash"
                FROM "Store Manager"
            """)
            store_managers = db.cursor.fetchall()
            return store_managers
        except Exception as e:
            print(f"Error retrieving store managers: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

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
    def manage_responsibilities(cls, store_manager_id: int):
        """Manage store manager responsibilities through a menu."""
        while True:
            print("\nResponsibility Management")
            print("1. Add Responsibility")
            print("2. Remove Responsibility")
            print("3. View Responsibilities")
            print("4. Back")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                cls.add_responsibility(store_manager_id)
            elif choice == '2':
                cls.remove_responsibility(store_manager_id)
            elif choice == '3':
                cls.view_responsibilities(store_manager_id)
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")

    @classmethod
    def add_responsibility(cls, store_manager_id: int):
        """Add a new responsibility to a store manager."""
        db = DBEngine()
        try:
            responsibility_id = int(input("Enter responsibility ID to add: ").strip())
            db.cursor.execute("""
                INSERT INTO "SM Responsibilities" ("ResponsibilityID", "StoreManagerID")
                VALUES (%s, %s)
            """, (responsibility_id, store_manager_id))
            db.connection.commit()
            print(f"Responsibility {responsibility_id} added to store manager {store_manager_id}.")
        except ValueError:
            print("Invalid responsibility ID. Please enter a number.")
        except Exception as e:
            print(f"Error adding responsibility: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def remove_responsibility(cls, store_manager_id: int):
        """Remove a responsibility from a store manager."""
        db = DBEngine()
        try:
            responsibility_id = int(input("Enter responsibility ID to remove: ").strip())
            db.cursor.execute('DELETE FROM "SM Responsibilities" WHERE "ResponsibilityID" = %s AND "StoreManagerID" = %s',
                              (responsibility_id, store_manager_id))
            db.connection.commit()
            print(f"Responsibility {responsibility_id} removed from store manager {store_manager_id}.")
        except ValueError:
            print("Invalid responsibility ID. Please enter a number.")
        except Exception as e:
            print(f"Error removing responsibility: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def view_responsibilities(cls, store_manager_id: int):
        """View responsibilities for a specific store manager."""
        db = DBEngine()
        try:
            db.cursor.execute('SELECT * FROM "SM Responsibilities" WHERE "StoreManagerID" = %s', (store_manager_id,))
            responsibilities = db.cursor.fetchall()
            if responsibilities:
                print(f"\nResponsibilities for Store Manager ID: {store_manager_id}")
                for resp in responsibilities:
                    print(f"Responsibility ID: {resp[0]}")
            else:
                print("No responsibilities found for this store manager.")
        except Exception as e:
            print(f"Error retrieving responsibilities: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

def manage_store_manager_menu():
    """Store Manager management menu with all options."""
    while True:
        print("\nStore Manager Management")
        print("1. Add Store Manager")
        print("2. Edit Store Manager")
        print("3. Delete Store Manager")
        print("4. View All Store Managers")
        print("5. Display All Salaries")
        print("6. Manage Responsibilities")
        print("7. Back")

        choice = input("Enter your choice (1-7): ")

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
            try:
                manager_id = int(input("Enter Store Manager ID to manage responsibilities: ").strip())
                StoreManager.manage_responsibilities(manager_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == '7':
            break
        else:
            print("Invalid choice, please select between 1 and 7.")

def add_store_manager():
    """Add a new store manager."""
    try:
        name = input("Enter store manager's name: ").strip()
        phone = int(input("Enter store manager's phone number: ").strip())
        email = input("Enter store manager's email: ").strip()
        country = input("Enter store manager's country: ").strip()
        store_id = int(input("Enter store ID: ").strip())
        monthly_salary = int(input("Enter store manager's monthly salary: ").strip())
        petty_cash = int(input("Enter store manager's petty cash: ").strip())

        store_manager = StoreManager(name, phone, email, country, store_id, monthly_salary, petty_cash)
        store_manager.save()
        print("Store Manager added successfully.")
    except ValueError:
        print("Invalid input. Please enter the correct data type.")

def edit_store_manager():
    """Edit an existing store manager."""
    try:
        manager_id = int(input("Enter the ID of the store manager to edit: ").strip())
        db = DBEngine()
        db.cursor.execute('SELECT * FROM "Store Manager" WHERE "StoreManagerID" = %s', (manager_id,))
        sm_data = db.cursor.fetchone()
        if sm_data:
            name = input(f"Enter new name (current: {sm_data[2]}): ").strip() or sm_data[2]
            phone = input(f"Enter new phone number (current: {sm_data[5]}): ").strip()
            phone = int(phone) if phone else sm_data[5]
            email = input(f"Enter new email (current: {sm_data[4]}): ").strip() or sm_data[4]
            country = input(f"Enter new country (current: {sm_data[3]}): ").strip() or sm_data[3]
            store_id = input(f"Enter new store ID (current: {sm_data[1]}): ").strip()
            store_id = int(store_id) if store_id else sm_data[1]
            monthly_salary = input(f"Enter new monthly salary (current: {sm_data[6]}): ").strip()
            monthly_salary = int(monthly_salary) if monthly_salary else sm_data[6]
            petty_cash = input(f"Enter new petty cash (current: {sm_data[7]}): ").strip()
            petty_cash = int(petty_cash) if petty_cash else sm_data[7]

            store_manager = StoreManager(name, phone, email, country, store_id, monthly_salary, petty_cash, manager_id)
            store_manager.save()
            print("Store Manager updated successfully.")
        else:
            print("Store Manager not found.")
    except ValueError:
        print("Invalid input. Please enter the correct data type.")
    except Exception as e:
        print(f"Error editing store manager: {e}")
    finally:
        db.cursor.close()
        db.connection.close()

def delete_store_manager():
    """Delete an existing store manager."""
    try:
        manager_id = int(input("Enter the ID of the store manager to delete: ").strip())
        store_manager = StoreManager(name='', phone=0, email='', country='', store_id=0, monthly_salary=0, petty_cash=0, id=manager_id)
        store_manager.delete()
        print("Store Manager deleted successfully.")
    except ValueError:
        print("Invalid ID. Please enter a number.")

def view_all_store_managers():
    """View all store managers."""
    store_managers = StoreManager.view_all()
    if store_managers:
        for sm in store_managers:
            print(f"ID: {sm[0]}, Store ID: {sm[1]}, Name: {sm[2]}, Country: {sm[3]}, Email: {sm[4]}, Phone: {sm[5]}, Monthly Salary: {sm[6]}, Petty Cash: {sm[7]}")
    else:
        print("No store managers found.")

def display_all_salaries():
    """Display all store managers' salaries."""
    StoreManager.display_all_salaries()
