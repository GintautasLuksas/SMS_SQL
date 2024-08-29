from typing import Optional, List, Tuple
from src.db_engine import DBEngine
from src.person.person import Person

class Manager(Person):
    """Represents a manager in a store, extending from Person."""

    def __init__(self, name: str, phone: int, email: str, country: str, monthly_salary: int, store_id: int,
                 id: Optional[int] = None) -> None:
        """Initialize a new Manager instance.

        Args:
            name (str): The manager's name.
            phone (int): The manager's phone number.
            email (str): The manager's email address.
            country (str): The country where the manager is based.
            monthly_salary (int): The manager's monthly salary.
            store_id (int): The ID of the store where the manager works.
            id (Optional[int]): The manager's ID in the database. Defaults to None.
        """
        super().__init__(name, phone, email, country, id)
        self.monthly_salary = monthly_salary
        self.store_id = store_id

    def display_salary(self) -> None:
        """Display the manager's monthly salary."""
        print(f"{self.name}'s monthly salary is: {self.monthly_salary}")

    def save(self) -> None:
        """Save a new manager or update an existing manager in the database."""
        if self.id is None:
            self._create_manager()
        else:
            self._update_manager()

    def _create_manager(self) -> None:
        """Insert a new manager into the database."""
        with DBEngine() as db:
            if db.cursor and db.connection:
                try:
                    db.cursor.execute(
                        """
                        INSERT INTO "Manager" ("Name", "PhoneNumber", "Email", "Country", "MonthlySalary", "StoreID")
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING "ManagerID"
                        """,
                        (self.name, self.phone, self.email, self.country, self.monthly_salary, self.store_id)
                    )
                    self.id = db.cursor.fetchone()[0]
                    db.connection.commit()
                    print("Manager created successfully.")
                except Exception as e:
                    print(f"Error creating manager: {e}")

    def _update_manager(self) -> None:
        """Update an existing manager's information."""
        if self.id is None:
            raise ValueError("Cannot update manager without an ID.")

        with DBEngine() as db:
            if db.cursor and db.connection:
                try:
                    sql_query = (
                        """
                        UPDATE "Manager"
                        SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s,
                        "Country" = %s, "MonthlySalary" = %s, "StoreID" = %s
                        WHERE "ManagerID" = %s
                        """
                    )
                    db.cursor.execute(
                        sql_query,
                        (self.name, self.phone, self.email, self.country, self.monthly_salary, self.store_id, self.id)
                    )
                    db.connection.commit()
                    print("Manager updated successfully.")
                except Exception as e:
                    print(f"Error updating manager: {e}")

    def delete(self) -> None:
        """Delete a manager from the database."""
        if self.id is not None:
            with DBEngine() as db:
                if db.cursor and db.connection:
                    try:
                        db.cursor.execute('DELETE FROM "Manager" WHERE "ManagerID" = %s', (self.id,))
                        db.connection.commit()
                        self.id = None
                        print("Manager deleted successfully.")
                    except Exception as e:
                        print(f"Error deleting manager: {e}")

    @classmethod
    def view_all(cls) -> None:
        """View all managers in the table."""
        with DBEngine() as db:
            if db.cursor and db.connection:
                try:
                    db.cursor.execute(
                        """
                        SELECT "ManagerID", "Name", "PhoneNumber", "Email", "Country", "MonthlySalary", "StoreID"
                        FROM "Manager"
                        """
                    )
                    managers = db.cursor.fetchall()
                    if managers:
                        print("List of All Managers:")
                        for row in managers:
                            print(
                                f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}, Email: {row[3]}, Country: {row[4]}, Salary: {row[5]}, Store ID: {row[6]}"
                            )
                    else:
                        print("No managers found.")
                except Exception as e:
                    print(f"Error retrieving managers: {e}")

    @classmethod
    def display_all_salaries(cls) -> None:
        """Display all managers' salaries."""
        cls.view_all()  # Ensure view_all is called to display manager details including salaries.

    @classmethod
    def manage_managers(cls) -> None:
        """Manage managers through a menu."""
        while True:
            print("\nManager Management Menu")
            print("1. Add Manager")
            print("2. Edit Manager")
            print("3. Delete Manager")
            print("4. View All Managers")
            print("5. Display All Salaries")
            print("6. Manage Responsibilities")
            print("7. Back")

            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                cls.add_manager()
            elif choice == '2':
                cls.edit_manager()
            elif choice == '3':
                cls.delete_manager()
            elif choice == '4':
                cls.view_all()  # Directly use the updated view_all method.
            elif choice == '5':
                cls.display_all_salaries()
            elif choice == '6':
                print("Manage Responsibilities feature is not implemented yet.")
            elif choice == '7':
                break
            else:
                print("Invalid choice, please select between 1 and 7.")

    @classmethod
    def add_manager(cls) -> None:
        """Add a new manager."""
        try:
            name = input("Enter manager's name: ").strip()
            phone = int(input("Enter manager's phone number: ").strip())
            email = input("Enter manager's email: ").strip()
            country = input("Enter manager's country: ").strip()
            monthly_salary = int(input("Enter manager's monthly salary: ").strip())
            store_id = int(input("Enter store ID: ").strip())

            manager = cls(name, phone, email, country, monthly_salary, store_id)
            manager.save()
            print("Manager added successfully.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")

    @classmethod
    def edit_manager(cls) -> None:
        """Edit an existing manager."""
        try:
            manager_id = int(input("Enter the ID of the manager to edit: ").strip())
            with DBEngine() as db:
                if db.cursor and db.connection:
                    db.cursor.execute('SELECT * FROM "Manager" WHERE "ManagerID" = %s', (manager_id,))
                    manager_data = db.cursor.fetchone()
                    if manager_data:
                        name = input(f"Enter new name (current: {manager_data[1]}): ").strip() or manager_data[1]
                        phone_input = input(f"Enter new phone number (current: {manager_data[2]}): ").strip()
                        phone = int(phone_input) if phone_input else manager_data[2]
                        email = input(f"Enter new email (current: {manager_data[3]}): ").strip() or manager_data[3]
                        country = input(f"Enter new country (current: {manager_data[4]}): ").strip() or manager_data[4]
                        monthly_salary_input = input(f"Enter new monthly salary (current: {manager_data[5]}): ").strip()
                        monthly_salary = int(monthly_salary_input) if monthly_salary_input else manager_data[5]
                        store_id_input = input(f"Enter new store ID (current: {manager_data[6]}): ").strip()
                        store_id = int(store_id_input) if store_id_input else manager_data[6]

                        manager = cls(name, phone, email, country, monthly_salary, store_id, manager_id)
                        manager.save()
                        print("Manager updated successfully.")
                    else:
                        print("Manager not found.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")

    @classmethod
    def delete_manager(cls) -> None:
        """Delete an existing manager."""
        try:
            manager_id = int(input("Enter the ID of the manager to delete: ").strip())
            manager = cls("", 0, "", "", 0, 0, manager_id)
            manager.delete()
            print("Manager deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")
