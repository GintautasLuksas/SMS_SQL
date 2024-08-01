import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tables.worker_table import WorkerTable
from src.tables.manager_table import ManagerTable
from src.tables.store_manager_table import StoreManagerTable
from src.tables.food_table import FoodTable
from src.tables.dry_storage_table import DryStorageTable
from src.tables.responsibilities_table import ResponsibilitiesTable
from src.tables.manager_responsibilities_table import ManagerResponsibilitiesTable
from src.tables.sm_responsibilities_table import SMResponsibilitiesTable
from src.tables.store_table import StoreTable
from src.tables.store_dry_product_table import StoreDryProductTable
from src.tables.store_food_product_table import StoreFoodProductTable

# People management menus
def display_people_menu():
    """Display the people menu options."""
    print("\nPeople Management")
    print("1. Workers")
    print("2. Managers")
    print("3. Store Managers")
    print("4. Back")

def display_products_menu():
    """Display the products menu options."""
    print("\nProducts Management")
    print("1. Food")
    print("2. Dry Storage")
    print("3. Back")

def display_responsibilities_menu():
    """Display the responsibilities menu options."""
    print("\nResponsibilities Management")
    print("1. Responsibilities")
    print("2. Manager Responsibilities")
    print("3. SM Responsibilities")
    print("4. Back")

def display_store_menu():
    """Display the store menu options."""
    print("\nStore Management")
    print("1. Store")
    print("2. Store Dry Products")
    print("3. Store Food Products")
    print("4. Back")

def display_main_menu():
    """Display the main menu options."""
    print("\nMain Menu")
    print("1. People")
    print("2. Products")
    print("3. Responsibilities")
    print("4. Store")
    print("5. Exit")

def manage_workers():
    worker_table = WorkerTable()
    worker_table.manage_workers()

def manage_managers():
    manager_table = ManagerTable()
    manager_table.manage_managers()

def manage_store_managers():
    store_manager_table = StoreManagerTable()
    store_manager_table.manage_store_managers()

def manage_food():
    food_table = FoodTable()
    food_table.manage_food()

def manage_dry_storage():
    dry_storage_table = DryStorageTable()
    dry_storage_table.manage_dry_storage()

def manage_responsibilities():
    responsibilities_table = ResponsibilitiesTable()
    responsibilities_table.manage_responsibilities()

def manage_manager_responsibilities():
    manager_responsibilities_table = ManagerResponsibilitiesTable()
    manager_responsibilities_table.manage_manager_responsibilities()

def manage_sm_responsibilities():
    sm_responsibilities_table = SMResponsibilitiesTable()
    sm_responsibilities_table.manage_sm_responsibilities()

def manage_store():
    store_table = StoreTable()
    store_table.manage_stores()

def manage_store_dry_products():
    store_dry_product_table = StoreDryProductTable()
    store_dry_product_table.manage_store_dry_products()

def manage_store_food_products():
    store_food_product_table = StoreFoodProductTable()
    store_food_product_table.manage_store_food_products()

def main():
    while True:
        display_main_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            while True:
                display_people_menu()
                people_choice = input("Enter your choice (1-4): ")

                if people_choice == '1':
                    manage_workers()
                elif people_choice == '2':
                    manage_managers()
                elif people_choice == '3':
                    manage_store_managers()
                elif people_choice == '4':
                    break
                else:
                    print("Invalid choice, please select between 1 and 4.")

        elif choice == '2':
            while True:
                display_products_menu()
                products_choice = input("Enter your choice (1-3): ")

                if products_choice == '1':
                    manage_food()
                elif products_choice == '2':
                    manage_dry_storage()
                elif products_choice == '3':
                    break
                else:
                    print("Invalid choice, please select between 1 and 3.")

        elif choice == '3':
            while True:
                display_responsibilities_menu()
                responsibilities_choice = input("Enter your choice (1-4): ")

                if responsibilities_choice == '1':
                    manage_responsibilities()
                elif responsibilities_choice == '2':
                    manage_manager_responsibilities()
                elif responsibilities_choice == '3':
                    manage_sm_responsibilities()
                elif responsibilities_choice == '4':
                    break
                else:
                    print("Invalid choice, please select between 1 and 4.")

        elif choice == '4':
            while True:
                display_store_menu()
                store_choice = input("Enter your choice (1-4): ")

                if store_choice == '1':
                    manage_store()
                elif store_choice == '2':
                    manage_store_dry_products()
                elif store_choice == '3':
                    manage_store_food_products()
                elif store_choice == '4':
                    break
                else:
                    print("Invalid choice, please select between 1 and 4.")

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please select between 1 and 5.")

if __name__ == "__main__":
    main()
