import sys
from src.person.manager import Manager
from src.person.worker import Worker
from src.product.product import manage_dry_storage_items, manage_food_items
from src.person.storemanager import manage_store_manager_menu
from src.store.store import manage_store_menu
from src.list_tables import list_tables

def main_menu():
    """Display the main menu and handle user input."""
    while True:
        print("\nMain Menu")
        print("1. Store")
        print("2. People")
        print("3. Products")
        print("4. View Database Structure")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            store_menu()
        elif choice == '2':
            people_menu()
        elif choice == '3':
            product_menu()
        elif choice == '4':
            structure_menu()
        elif choice == '5':
            print("Exiting the application.")
            sys.exit()
        else:
            print("Invalid choice, please select between 1 and 5.")

def store_menu():
    """Display the store menu and handle user input."""
    while True:
        print("\nStore Menu")
        print("1. Manage Stores")
        print("2. Manage Store Products")
        print("3. Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            manage_store_menu()
        elif choice == '2':
            manage_store_items_menu()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")

def people_menu():
    """Display the people menu and handle user input."""
    while True:
        print("\nPeople Menu")
        print("1. Manage Managers")
        print("2. Manage Workers")
        print("3. Manage Store Managers")
        print("4. Back")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            Manager.manage_managers()
        elif choice == '2':
            Worker.manage_workers()
        elif choice == '3':
            manage_store_manager_menu()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please select between 1 and 4.")

def product_menu():
    """Display the product menu and handle user input."""
    while True:
        print("\nProduct Menu")
        print("1. Manage Dry Storage Items")
        print("2. Manage Food Items")
        print("3. Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            manage_dry_storage_items()
        elif choice == '2':
            manage_food_items()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")

def structure_menu():
    """Display database structure."""
    list_tables()

if __name__ == "__main__":
    main_menu()
