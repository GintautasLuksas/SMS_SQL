import os
import sys

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tables.store_manager_table import StoreManagerTable

def display_menu():
    """Display the menu options."""
    print("\nStore Manager Table Management")
    print("1. Add a new store manager")
    print("2. Edit an existing store manager")
    print("3. Delete a store manager")
    print("4. View all store managers")
    print("5. Exit")

def add_store_manager(store_manager_table):
    """Add a new store manager to the table."""
    try:
        store_id = int(input("Enter store ID: "))
        name = input("Enter store manager's name: ")
        country = input("Enter store manager's country: ")
        email = input("Enter store manager's email: ")
        phone_number = int(input("Enter store manager's phone number: "))
        sm_responsibility_id = int(input("Enter store manager's responsibility ID: "))
        monthly_salary = int(input("Enter store manager's monthly salary: "))
        petty_cash = int(input("Enter store manager's petty cash: "))

        store_manager_table.insert_data((store_id, name, country, email, phone_number, sm_responsibility_id, monthly_salary, petty_cash))
        print("Store manager added successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error adding store manager: {e}")

def edit_store_manager(store_manager_table):
    """Edit an existing store manager's information."""
    try:
        store_manager_id = int(input("Enter the store manager ID to edit: "))
        store_id = input("Enter new store ID (leave empty to keep current): ")
        name = input("Enter new name (leave empty to keep current): ")
        country = input("Enter new country (leave empty to keep current): ")
        email = input("Enter new email (leave empty to keep current): ")
        phone_number = input("Enter new phone number (leave empty to keep current): ")
        sm_responsibility_id = input("Enter new responsibility ID (leave empty to keep current): ")
        monthly_salary = input("Enter new monthly salary (leave empty to keep current): ")
        petty_cash = input("Enter new petty cash (leave empty to keep current): ")

        # Collect only fields that are not empty
        new_values = {}
        if store_id:
            new_values['StoreID'] = int(store_id)
        if name:
            new_values['Name'] = name
        if country:
            new_values['Country'] = country
        if email:
            new_values['Email'] = email
        if phone_number:
            new_values['PhoneNumber'] = int(phone_number)
        if sm_responsibility_id:
            new_values['SMResponsibilityID'] = int(sm_responsibility_id)
        if monthly_salary:
            new_values['MonthlySalary'] = int(monthly_salary)
        if petty_cash:
            new_values['PettyCash'] = int(petty_cash)

        if new_values:
            store_manager_table.update_data(store_manager_id, new_values)
            print("Store manager updated successfully!")
        else:
            print("No changes were made.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error updating store manager: {e}")

def delete_store_manager(store_manager_table):
    """Delete a store manager from the table."""
    try:
        store_manager_id = int(input("Enter the store manager ID to delete: "))
        store_manager_table.delete_data(store_manager_id)
        print("Store manager deleted successfully!")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error deleting store manager: {e}")

def view_store_managers(store_manager_table):
    """View all store managers in the table."""
    try:
        store_managers = store_manager_table.select_all()
        if store_managers:
            print("\nStore Managers in the table:")
            for manager in store_managers:
                print(manager)
        else:
            print("No store managers found.")
    except Exception as e:
        print(f"Error retrieving store managers: {e}")

def main():
    store_manager_table = StoreManagerTable()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_store_manager(store_manager_table)
        elif choice == '2':
            edit_store_manager(store_manager_table)
        elif choice == '3':
            delete_store_manager(store_manager_table)
        elif choice == '4':
            view_store_managers(store_manager_table)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please select between 1 and 5.")

if __name__ == "__main__":
    main()
