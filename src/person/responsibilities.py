"""
Responsibilities management module.

This module defines the `Responsibilities` class for managing responsibilities in the database
and provides methods to add, remove, and view responsibilities.
"""

from typing import Optional, List
from src.db_engine import DBEngine


class Responsibilities:
    def __init__(self, responsibility_id: Optional[int] = None, responsibility_name: Optional[str] = None) -> None:
        self.responsibility_id = responsibility_id
        self.responsibility_name = responsibility_name

    def save(self) -> None:
        """Save a new responsibility or update an existing one in the database."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor

        if connection is None or cursor is None:
            print("Database connection or cursor is not available.")
            return

        try:
            if self.responsibility_id is None:
                cursor.execute("""
                    INSERT INTO "Responsibilities" ("ResponsibilityName")
                    VALUES (%s)
                    RETURNING "ResponsibilityID"
                """, (self.responsibility_name,))
                self.responsibility_id = cursor.fetchone()[0]
                connection.commit()
                print(f"Responsibility '{self.responsibility_name}' added with ID {self.responsibility_id}.")
            else:
                cursor.execute("""
                    UPDATE "Responsibilities"
                    SET "ResponsibilityName" = %s
                    WHERE "ResponsibilityID" = %s
                """, (self.responsibility_name, self.responsibility_id))
                connection.commit()
                print(f"Responsibility ID {self.responsibility_id} updated to '{self.responsibility_name}'.")
        except Exception as e:
            print(f"Error saving responsibility: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete(self) -> None:
        """Delete a responsibility from the database."""
        if self.responsibility_id is not None:
            db = DBEngine()
            connection = db.connection
            cursor = db.cursor

            if connection is None or cursor is None:
                print("Database connection or cursor is not available.")
                return

            try:
                cursor.execute('DELETE FROM "Responsibilities" WHERE "ResponsibilityID" = %s',
                               (self.responsibility_id,))
                connection.commit()
                print(f"Responsibility ID {self.responsibility_id} deleted.")
                self.responsibility_id = None
            except Exception as e:
                print(f"Error deleting responsibility: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            print("Responsibility ID is not set.")

    @classmethod
    def view_all(cls) -> List['Responsibilities']:
        """View all responsibilities in the table."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor

        if connection is None or cursor is None:
            print("Database connection or cursor is not available.")
            return []

        try:
            cursor.execute('SELECT "ResponsibilityID", "ResponsibilityName" FROM "Responsibilities"')
            responsibilities = cursor.fetchall()
            return [cls(responsibility_id=res[0], responsibility_name=res[1]) for res in responsibilities]
        except Exception as e:
            print(f"Error retrieving responsibilities: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def add_sm_responsibility(responsibility_id: int, store_manager_id: int) -> None:
        """Assign a responsibility to a store manager."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor

        if connection is None or cursor is None:
            print("Database connection or cursor is not available.")
            return

        try:
            cursor.execute("""
                INSERT INTO "SM Responsibilities" ("ResponsibilityID", "StoreManagerID")
                VALUES (%s, %s)
            """, (responsibility_id, store_manager_id))
            connection.commit()
            print(f"Responsibility {responsibility_id} assigned to Store Manager {store_manager_id}.")
        except Exception as e:
            print(f"Error assigning responsibility: {e}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def remove_sm_responsibility(responsibility_id: int, store_manager_id: int) -> None:
        """Remove a responsibility from a store manager."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor

        if connection is None or cursor is None:
            print("Database connection or cursor is not available.")
            return

        try:
            cursor.execute("""
                DELETE FROM "SM Responsibilities"
                WHERE "ResponsibilityID" = %s AND "StoreManagerID" = %s
            """, (responsibility_id, store_manager_id))
            connection.commit()
            print(f"Responsibility {responsibility_id} removed from Store Manager {store_manager_id}.")
        except Exception as e:
            print(f"Error removing responsibility: {e}")
        finally:
            cursor.close()
            connection.close()


def responsibilities_menu() -> None:
    """Responsibilities management menu with all options."""
    while True:
        print("\nResponsibilities Management")
        print("1. Add Responsibility")
        print("2. Remove Responsibility")
        print("3. Assign Responsibility to Store Manager")
        print("4. Remove Responsibility from Store Manager")
        print("5. View Responsibilities")
        print("6. Back")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            add_responsibility()
        elif choice == '2':
            remove_responsibility()
        elif choice == '3':
            assign_responsibility_to_manager()
        elif choice == '4':
            remove_responsibility_from_manager()
        elif choice == '5':
            view_responsibilities()
        elif choice == '6':
            break
        else:
            print("Invalid choice, please select between 1 and 6.")


def add_responsibility() -> None:
    """Add a new responsibility to the database."""
    responsibility_name = input("Enter the responsibility name: ").strip()
    responsibility = Responsibilities(responsibility_name=responsibility_name)
    responsibility.save()


def remove_responsibility() -> None:
    """Remove a responsibility from the database."""
    try:
        responsibility_id = int(input("Enter the ID of the responsibility to delete: ").strip())
        responsibility = Responsibilities(responsibility_id=responsibility_id)
        responsibility.delete()
    except ValueError:
        print("Invalid ID. Please enter a number.")


def assign_responsibility_to_manager() -> None:
    """Assign a responsibility to a store manager."""
    try:
        responsibility_id = int(input("Enter the responsibility ID to assign: ").strip())
        store_manager_id = int(input("Enter the Store Manager ID: ").strip())
        Responsibilities.add_sm_responsibility(responsibility_id, store_manager_id)
    except ValueError:
        print("Invalid input. Please enter numbers.")


def remove_responsibility_from_manager() -> None:
    """Remove a responsibility from a store manager."""
    try:
        responsibility_id = int(input("Enter the responsibility ID to remove: ").strip())
        store_manager_id = int(input("Enter the Store Manager ID: ").strip())
        Responsibilities.remove_sm_responsibility(responsibility_id, store_manager_id)
    except ValueError:
        print("Invalid input. Please enter numbers.")


def view_responsibilities() -> None:
    """View all responsibilities."""
    responsibilities = Responsibilities.view_all()
    if responsibilities:
        print("\nResponsibilities:")
        for res in responsibilities:
            print(f"ID: {res.responsibility_id}, Name: {res.responsibility_name}")
    else:
        print("No responsibilities found.")
