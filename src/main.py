import sys
from src.person.person import Worker, Manager, StoreManager
from src.product.product import Food, DryStorage
from src.db_engine import DBEngine

class InteractiveSystem:
    def __init__(self):
        self.db = DBEngine()  # Initialize database connection

    def display_people_menu(self):
        print("\nPeople Management")
        print("1. Workers")
        print("2. Managers")
        print("3. Store Managers")
        print("4. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.manage_workers()
        elif choice == "2":
            self.manage_managers()
        elif choice == "3":
            self.manage_store_managers()
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

    def display_products_menu(self):
        print("\nProducts Management")
        print("1. Food")
        print("2. Dry Storage")
        print("3. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.manage_food_products()
        elif choice == "2":
            self.manage_dry_storage_products()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

    def display_responsibilities_menu(self):
        print("\nResponsibilities Management")
        print("1. Responsibilities")
        print("2. SM Responsibilities")
        print("3. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.manage_responsibilities()
        elif choice == "2":
            self.manage_sm_responsibilities()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")

    def display_store_menu(self):
        print("\nStore Management")
        print("1. Store")
        print("2. Store Dry Products")
        print("3. Store Food Products")
        print("4. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.manage_store()
        elif choice == "2":
            self.manage_store_dry_products()
        elif choice == "3":
            self.manage_store_food_products()
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

    def display_main_menu(self):
        print("\nMain Menu")
        print("1. People")
        print("2. Products")
        print("3. Responsibilities")
        print("4. Store")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            self.display_people_menu()
        elif choice == "2":
            self.display_products_menu()
        elif choice == "3":
            self.display_responsibilities_menu()
        elif choice == "4":
            self.display_store_menu()
        elif choice == "5":
            sys.exit("Exiting the system.")
        else:
            print("Invalid choice. Please try again.")

    def manage_workers(self):
        print("\nManage Workers")
        # Add, update, delete, or list workers
        # Example:
        self.add_worker()  # or self.update_worker(), self.delete_worker()

    def manage_managers(self):
        print("\nManage Managers")
        # Add, update, delete, or list managers
        # Example:
        self.add_manager()  # or self.update_manager(), self.delete_manager()

    def manage_store_managers(self):
        print("\nManage Store Managers")
        # Add, update, delete, or list store managers
        # Example:
        self.add_store_manager()  # or self.update_store_manager(), self.delete_store_manager()

    def manage_food_products(self):
        print("\nManage Food Products")
        # Add, update, delete, or list food products
        # Example:
        self.add_food_product()  # or self.update_food_product(), self.delete_food_product()

    def manage_dry_storage_products(self):
        print("\nManage Dry Storage Products")
        # Add, update, delete, or list dry storage products
        # Example:
        self.add_dry_storage_product()  # or self.update_dry_storage_product(), self.delete_dry_storage_product()

    def manage_responsibilities(self):
        print("\nManage Responsibilities")
        # Add, update, delete, or list responsibilities
        # Example:
        pass  # Implement functionality as needed

    def manage_sm_responsibilities(self):
        print("\nManage SM Responsibilities")
        # Add, update, delete, or list SM responsibilities
        # Example:
        pass  # Implement functionality as needed

    def manage_store(self):
        print("\nManage Store")
        # Add, update, delete, or list store-related functionalities
        # Example:
        pass  # Implement functionality as needed

    def manage_store_dry_products(self):
        print("\nManage Store Dry Products")
        # Add, update, delete, or list store dry products
        # Example:
        pass  # Implement functionality as needed

    def manage_store_food_products(self):
        print("\nManage Store Food Products")
        # Add, update, delete, or list store food products
        # Example:
        pass  # Implement functionality as needed

    def add_worker(self):
        name = input("Enter name: ")
        phone = int(input("Enter phone: "))
        email = input("Enter email: ")
        country = input("Enter country: ")
        hourly_rate = float(input("Enter hourly rate: "))
        amount_worked = int(input("Enter amount worked: "))
        worker = Worker(name, phone, email, country, hourly_rate, amount_worked)
        worker.save()  # Implement save method in Worker class
        print(f"Worker {worker.name} added.")

    def add_manager(self):
        name = input("Enter name: ")
        phone = int(input("Enter phone: "))
        email = input("Enter email: ")
        country = input("Enter country: ")
        salary = int(input("Enter salary: "))
        responsibility = input("Enter responsibility: ")
        manager = Manager(name, phone, email, country, salary, responsibility)
        manager.save()  # Implement save method in Manager class
        print(f"Manager {manager.name} added.")

    def add_store_manager(self):
        name = input("Enter name: ")
        phone = int(input("Enter phone: "))
        email = input("Enter email: ")
        country = input("Enter country: ")
        monthly_salary = int(input("Enter monthly salary: "))
        store_name = input("Enter store name: ")
        responsibilities = input("Enter responsibilities (comma-separated): ").split(',')
        petty_cash = int(input("Enter petty cash: "))
        store_manager = StoreManager(name, phone, email, country, monthly_salary, store_name, responsibilities, petty_cash)
        store_manager.save()  # Implement save method in StoreManager class
        print(f"Store Manager {store_manager.name} added.")

    def add_food_product(self):
        name = input("Enter product name: ")
        price = int(input("Enter price: "))
        amount = int(input("Enter amount: "))
        item_code = int(input("Enter item code: "))
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
        storage_conditions = input("Enter storage conditions: ")
        food = Food(name, price, amount, item_code, expiry_date, storage_conditions)
        food.add_item()  # Implement add_item method to save to database
        print(f"Food product {food.name} added.")

    def add_dry_storage_product(self):
        name = input("Enter product name: ")
        price = int(input("Enter price: "))
        amount = int(input("Enter amount: "))
        item_code = int(input("Enter item code: "))
        is_recipe = input("Is it a recipe product (True/False): ") == 'True'
        is_chemical = input("Is it a chemical product (True/False): ") == 'True'
        package = input("Enter package type: ")
        dry_storage = DryStorage(name, price, amount, item_code, is_recipe, is_chemical, package)
        dry_storage.add_item()  # Implement add_item method to save to database
        print(f"Dry Storage product {dry_storage.name} added.")

def main():
    system = InteractiveSystem()
    while True:
        system.display_main_menu()

if __name__ == "__main__":
    main()
