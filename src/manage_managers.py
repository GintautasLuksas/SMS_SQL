import os
import sys

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tables.manager_table import ManagerTable

def display_menu():
    """Display the menu options."""
    print("\nManager Table Management")
    print("1. Add a new manager")
    print("2. Edit an existing manager")
    print("3. Delete a manager")
    print("4. View all managers")
    print("5. Exit")

def add_manager(manager_table):
    """Add a new manager to the table."""
    try:
        name = input("Enter manager's name: ")
        phone_number = int(input("Enter manager's phone number: "))
        country = input("Enter manager's country: ")
        email = input("Enter manager's email: ")
        monthly_salary = int(input("Enter manager's monthly salary: "))
        mgr_responsibility_id = int(input("Enter manager's responsibility ID: "))

        manager_table.insert_data((name, phone_number, country, email, monthly_salary, mgr_responsibility_id))
        print("Manager added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error adding manager: {e}")

def edit_manager(manager_table):
    """Edit an existing manager's information."""
    try:
        manager_id = int(input("Enter the manager ID to edit: "))
        name = input("Enter new name (leave empty to keep current): ")
        phone_number = input("Enter new phone number (leave empty to keep current): ")
        country = input("Enter new country (leave empty to keep current): ")
        email = input("Enter new email (leave empty to keep current): ")
        monthly_salary = input("Enter new monthly salary (leave empty to keep current): ")
        mgr_responsibility_id = input("Enter new responsibility ID (leave empty to keep current): ")

        # Collect only fields that are not empty
        new_values = {}
        if name:
            new_values['Name'] = name
        if phone_number:
            new_values['PhoneNumber'] = int(phone_number)
        if country:
            new_values['Country'] = country
        if email:
            new_values['Email'] = email
        if monthly_salary:
            new_values['MonthlySalary'] = int(monthly_salary)
        if mgr_responsibility_id:
            new_values['MGRResponibilityID'] = int(mgr_responsibility_id)

        if new_values:
            manager_table.update_data(manager_id, new_values)
            print("Manager updated successfully!")
        else:
            print("No changes were made.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error updating manager: {e}")

def delete_manager(manager_table):
    """Delete a manager from the table."""
    try:
        manager_id = int(input("Enter the manager ID to delete: "))
        manager_table.delete_data(manager_id)
        print("Manager deleted successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error deleting manager: {e}")

def view_managers(manager_table):
    """View all managers in the table."""
    try:
        managers = manager_table.select_all()
        if managers:
            print("\nManagers in the table:")
            for manager in managers:
                print(manager)
        else:
            print("No managers found.")
    except Exception as e:
        print(f"Error retrieving managers: {e}")

def main():
    manager_table = ManagerTable()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_manager(manager_table)
        elif choice == '2':
            edit_manager(manager_table)
        elif choice == '3':
            delete_manager(manager_table)
        elif choice == '4':
            view_managers(manager_table)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select between 1 and 5.")

if __name__ == "__main__":
    main()
