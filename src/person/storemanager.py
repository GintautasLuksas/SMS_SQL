from typing import Optional
from src.db_engine import DBEngine
from src.person.person import Person

class StoreManager(Person):
    """Represents a store manager in the system."""

    def __init__(self, name: str, phone: int, email: str, country: str, store_id: int,
                 monthly_salary: int, petty_cash: int, id: Optional[int] = None) -> None:
        """Initialize a new store manager with the given details.

        Args:
            name (str): The name of the store manager.
            phone (int): The phone number of the store manager.
            email (str): The email address of the store manager.
            country (str): The country of the store manager.
            store_id (int): The ID of the store where the manager works.
            monthly_salary (int): The monthly salary of the store manager.
            petty_cash (int): The petty cash amount for the store manager.
            id (Optional[int], optional): The unique identifier for the store manager. Defaults to None.
        """
        super().__init__(name, phone, email, country, id)
        self.store_id = store_id
        self.monthly_salary = monthly_salary
        self.petty_cash = petty_cash

    def display_salary(self) -> None:
        """Display the store manager's monthly salary."""
        print(f"{self.name}'s monthly salary is: {self.monthly_salary}")

    def save(self) -> None:
        """Save a new store manager or update an existing store manager in the database."""
        if self.id is None:
            self._create_store_manager()
        else:
            self._update_store_manager()

    def _create_store_manager(self) -> None:
        """Insert a new store manager into the database."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        if cursor is None or connection is None:
            print("Database connection not established.")
            return
        try:
            cursor.execute("""
                INSERT INTO "Store Manager" ("StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "StoreManagerID"
            """, (self.store_id, self.name, self.country, self.email, self.phone, self.monthly_salary, self.petty_cash))
            self.id = cursor.fetchone()[0]
            connection.commit()
            print("Store Manager created successfully.")
        except Exception as e:
            print(f"Error creating store manager: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def _update_store_manager(self) -> None:
        """Update an existing store manager's information."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        if cursor is None or connection is None:
            print("Database connection not established.")
            return
        try:
            cursor.execute("""
                UPDATE "Store Manager"
                SET "StoreID" = %s, "Name" = %s, "Country" = %s, "Email" = %s, "PhoneNumber" = %s, "MonthlySalary" = %s, "PettyCash" = %s
                WHERE "StoreManagerID" = %s
            """, (self.store_id, self.name, self.country, self.email, self.phone, self.monthly_salary, self.petty_cash,
                  self.id))
            connection.commit()
            print("Store Manager updated successfully.")
        except Exception as e:
            print(f"Error updating store manager: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete(self) -> None:
        """Delete a store manager from the database."""
        if self.id is not None:
            db = DBEngine()
            connection = db.connection
            cursor = db.cursor
            if cursor is None or connection is None:
                print("Database connection not established.")
                return
            try:
                cursor.execute('DELETE FROM "Store Manager" WHERE "StoreManagerID" = %s', (self.id,))
                connection.commit()
                self.id = None
                print("Store Manager deleted successfully.")
            except Exception as e:
                print(f"Error deleting store manager: {e}")
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        else:
            print("Store Manager ID is not set.")

    @classmethod
    def view_all(cls) -> None:
        """View all store managers in the table."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        if cursor is None or connection is None:
            print("Database connection not established.")
            return
        try:
            cursor.execute("""
                SELECT "StoreManagerID", "StoreID", "Name", "Country", "Email", "PhoneNumber", "MonthlySalary", "PettyCash"
                FROM "Store Manager"
            """)
            store_managers = cursor.fetchall()
            if store_managers:
                print("List of All Store Managers:")
                for sm in store_managers:
                    print(
                        f"ID: {sm[0]}, StoreID: {sm[1]}, Name: {sm[2]}, Country: {sm[3]}, Email: {sm[4]}, Phone: {sm[5]}, Salary: {sm[6]}, Petty Cash: {sm[7]}")
            else:
                print("No store managers found.")
        except Exception as e:
            print(f"Error retrieving store managers: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def display_all_salaries(cls) -> None:
        """Display all store managers' salaries."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        if cursor is None or connection is None:
            print("Database connection not established.")
            return
        try:
            cursor.execute("""
                SELECT "StoreManagerID", "Name", "MonthlySalary"
                FROM "Store Manager"
            """)
            salaries = cursor.fetchall()
            if salaries:
                print("Salaries of All Store Managers:")
                for salary in salaries:
                    print(f"ID: {salary[0]}, Name: {salary[1]}, Salary: {salary[2]}")
            else:
                print("No store managers found.")
        except Exception as e:
            print(f"Error retrieving salaries: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

def manage_store_manager_menu() -> None:
    """Store Manager management menu with all options."""
    while True:
        print("\nStore Manager Management")
        print("1. Add Store Manager")
        print("2. Edit Store Manager")
        print("3. Delete Store Manager")
        print("4. View All Store Managers")
        print("5. Display All Salaries")
        print("6. Back")

        choice = input("Enter your choice (1-6): ")

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
            break
        else:
            print("Invalid choice, please select between 1 and 6.")

def add_store_manager() -> None:
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

def edit_store_manager() -> None:
    """Edit an existing store manager."""
    try:
        manager_id = int(input("Enter the ID of the store manager to edit: ").strip())
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        if cursor is None or connection is None:
            print("Database connection not established.")
            return
        try:
            cursor.execute('SELECT * FROM "Store Manager" WHERE "StoreManagerID" = %s', (manager_id,))
            sm_data = cursor.fetchone()
            if sm_data:
                name = input(f"Enter new name (current: {sm_data[2]}): ").strip() or sm_data[2]

                # Correctly handle phone input
                phone_input = input(f"Enter new phone number (current: {sm_data[5]}): ").strip()
                phone = int(phone_input) if phone_input else sm_data[5]

                email = input(f"Enter new email (current: {sm_data[4]}): ").strip() or sm_data[4]
                country = input(f"Enter new country (current: {sm_data[3]}): ").strip() or sm_data[3]
                store_id_input = input(f"Enter new store ID (current: {sm_data[1]}): ").strip()
                store_id = int(store_id_input) if store_id_input else sm_data[1]
                monthly_salary_input = input(f"Enter new monthly salary (current: {sm_data[6]}): ").strip()
                monthly_salary = int(monthly_salary_input) if monthly_salary_input else sm_data[6]
                petty_cash_input = input(f"Enter new petty cash (current: {sm_data[7]}): ").strip()
                petty_cash = int(petty_cash_input) if petty_cash_input else sm_data[7]

                store_manager = StoreManager(name, phone, email, country, store_id, monthly_salary, petty_cash, manager_id)
                store_manager.save()
                print("Store Manager updated successfully.")
            else:
                print("Store Manager not found.")
        except Exception as e:
            print(f"Error retrieving store manager: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    except ValueError:
        print("Invalid input. Please enter the correct data type.")

def delete_store_manager() -> None:
    """Delete a store manager."""
    try:
        manager_id = int(input("Enter the ID of the store manager to delete: ").strip())
        store_manager = StoreManager(name="", phone=0, email="", country="", store_id=0, monthly_salary=0, petty_cash=0, id=manager_id)
        store_manager.delete()
    except ValueError:
        print("Invalid input. Please enter the correct data type.")

def view_all_store_managers() -> None:
    """View all store managers."""
    StoreManager.view_all()

def display_all_salaries() -> None:
    """Display all store managers' salaries."""
    StoreManager.display_all_salaries()
