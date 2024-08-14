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
                INSERT INTO "Store Manager" ("Name", "PhoneNumber", "Email", "Country", "StoreID", "SMResponsibilityID", "MonthlySalary", "PettyCash")
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING "StoreManagerID"
            """, (self.name, self.phone, self.email, self.country, self.store_id, self.sm_responsibility_id, self.monthly_salary, self.petty_cash))
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
                print(f"ID: {sm[7]}, Name: {sm[1]}, Salary: {sm[6]}")
        else:
            print("No store managers found.")

    @classmethod
    def display_all_responsibilities(cls):
        """Display all store managers' responsibility IDs."""
        store_managers = cls.view_all()
        if store_managers:
            print("Responsibilities of All Store Managers:")
            for sm in store_managers:
                print(f"ID: {sm[7]}, Name: {sm[1]}, Responsibility ID: {sm[5]}")
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
