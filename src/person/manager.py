from src.db_engine import DBEngine
from src.person.person import Person

class Manager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, department: str, annual_salary: int, id: int = None):
        super().__init__(name, phone, email, country)
        self.department = department
        self.annual_salary = annual_salary
        self.id = id

    def display_salary(self):
        """Display the manager's annual salary."""
        print(f'{self.name}\'s annual salary is: {self.annual_salary}')

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
            db.cursor.execute("""
                INSERT INTO "Manager" ("Name", "PhoneNumber", "Email", "Country", "MonthlySalary", "StoreID")
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING "ManagerID"
            """, (self.name, self.phone, self.email, self.country, self.annual_salary, self.store_id))
            self.id = db.cursor.fetchone()[0]
            db.connection.commit()
            print("Manager created successfully.")
        except Exception as e:
            print(f"Error creating manager: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    def _update_manager(self):
        """Update an existing manager's information."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                UPDATE "Manager"
                SET "Name" = %s, "PhoneNumber" = %s, "Email" = %s, "Country" = %s, "MonthlySalary" = %s, "StoreID" = %s
                WHERE "ManagerID" = %s
            """, (self.name, self.phone, self.email, self.country, self.annual_salary, self.store_id, self.id))
            db.connection.commit()
            print("Manager updated successfully.")
        except Exception as e:
            print(f"Error updating manager: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    def delete(self):
        """Delete a manager from the database."""
        if self.id is not None:
            db = DBEngine()
            try:
                db.cursor.execute('DELETE FROM "Manager" WHERE "ManagerID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
                print("Manager deleted successfully.")
            except Exception as e:
                print(f"Error deleting manager: {e}")
            finally:
                db.cursor.close()
                db.connection.close()
        else:
            print("Manager ID is not set.")

    @classmethod
    def view_all(cls):
        """View all managers in the table."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                SELECT "ManagerID", "Name", "PhoneNumber", "Email", "Country", "MonthlySalary", "StoreID"
                FROM "Manager"
            """)
            managers = db.cursor.fetchall()
            return managers
        except Exception as e:
            print(f"Error retrieving managers: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def display_all_salaries(cls):
        """Display all managers' salaries."""
        managers = cls.view_all()
        if managers:
            print("Salaries of All Managers:")
            for m in managers:
                print(f"ID: {m[0]}, Name: {m[1]}, Salary: {m[5]}")
        else:
            print("No managers found.")

    @classmethod
    def manage_managers(cls):
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
                cls.view_all_managers()
            elif choice == '5':
                cls.display_all_salaries()
            elif choice == '6':
                manager_id = int(input("Enter Manager ID to manage responsibilities: ").strip())
                cls.manage_responsibilities(manager_id)
            elif choice == '7':
                break
            else:
                print("Invalid choice, please select between 1 and 7.")

    @classmethod
    def add_manager(cls):
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
    def edit_manager(cls):
        """Edit an existing manager."""
        try:
            manager_id = int(input("Enter the ID of the manager to edit: ").strip())
            db = DBEngine()
            db.cursor.execute('SELECT * FROM "Manager" WHERE "ManagerID" = %s', (manager_id,))
            manager_data = db.cursor.fetchone()
            if manager_data:
                name = input(f"Enter new name (current: {manager_data[1]}): ").strip() or manager_data[1]
                phone = input(f"Enter new phone number (current: {manager_data[2]}): ").strip()
                phone = int(phone) if phone else manager_data[2]
                email = input(f"Enter new email (current: {manager_data[3]}): ").strip() or manager_data[3]
                country = input(f"Enter new country (current: {manager_data[4]}): ").strip() or manager_data[4]
                monthly_salary = input(f"Enter new monthly salary (current: {manager_data[5]}): ").strip()
                monthly_salary = int(monthly_salary) if monthly_salary else manager_data[5]
                store_id = input(f"Enter new store ID (current: {manager_data[6]}): ").strip()
                store_id = int(store_id) if store_id else manager_data[6]

                manager = cls(name, phone, email, country, monthly_salary, store_id, manager_id)
                manager.save()
                print("Manager updated successfully.")
            else:
                print("Manager not found.")
        except ValueError:
            print("Invalid input. Please enter the correct data type.")
        except Exception as e:
            print(f"Error editing manager: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def delete_manager(cls):
        """Delete an existing manager."""
        try:
            manager_id = int(input("Enter the ID of the manager to delete: ").strip())
            manager = cls(name='', phone=0, email='', country='', department='', annual_salary=0, id=manager_id)
            manager.delete()
            print("Manager deleted successfully.")
        except ValueError:
            print("Invalid ID. Please enter a number.")

    @classmethod
    def view_all_managers(cls):
        """View all managers."""
        managers = cls.view_all()
        if managers:
            for manager in managers:
                print(f"ID: {manager[0]}, Name: {manager[1]}, Salary: {manager[5]}")
        else:
            print("No managers found.")

    @classmethod
    def manage_responsibilities(cls, manager_id: int):
        """Manage manager responsibilities through a menu."""
        while True:
            print("\nResponsibility Management")
            print("1. Add Responsibility")
            print("2. Remove Responsibility")
            print("3. View Responsibilities")
            print("4. Back")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == '1':
                cls.add_responsibility(manager_id)
            elif choice == '2':
                cls.remove_responsibility(manager_id)
            elif choice == '3':
                cls.view_responsibilities(manager_id)
            elif choice == '4':
                break
            else:
                print("Invalid choice, please select between 1 and 4.")

    @classmethod
    def add_responsibility(cls, manager_id: int):
        """Add a new responsibility to a manager."""
        db = DBEngine()
        try:
            responsibility_id = int(input("Enter responsibility ID to add: ").strip())
            db.cursor.execute("""
                INSERT INTO "SM Responsibilities" ("ResponsibilityID", "StoreManagerID")
                VALUES (%s, %s)
            """, (responsibility_id, manager_id))
            db.connection.commit()
            print(f"Responsibility {responsibility_id} added to manager {manager_id}.")
        except Exception as e:
            print(f"Error adding responsibility: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def remove_responsibility(cls, manager_id: int):
        """Remove a responsibility from a manager."""
        db = DBEngine()
        try:
            responsibility_id = int(input("Enter responsibility ID to remove: ").strip())
            db.cursor.execute('DELETE FROM "SM Responsibilities" WHERE "ResponsibilityID" = %s AND "StoreManagerID" = %s', (responsibility_id, manager_id))
            db.connection.commit()
            print(f"Responsibility {responsibility_id} removed from manager {manager_id}.")
        except Exception as e:
            print(f"Error removing responsibility: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @classmethod
    def view_responsibilities(cls, manager_id: int):
        """View all responsibilities for a specific manager."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                SELECT r."ResponsibilityName"
                FROM "SM Responsibilities" sr
                JOIN "Responsibilities" r ON sr."ResponsibilityID" = r."ResponsibilityID"
                WHERE sr."StoreManagerID" = %s
            """, (manager_id,))
            responsibilities = db.cursor.fetchall()
            if responsibilities:
                print(f"Responsibilities for Manager {manager_id}:")
                for r in responsibilities:
                    print(f"- {r[0]}")
            else:
                print(f"No responsibilities found for Manager {manager_id}.")
        except Exception as e:
            print(f"Error retrieving responsibilities: {e}")
        finally:
            db.cursor.close()
            db.connection.close()
