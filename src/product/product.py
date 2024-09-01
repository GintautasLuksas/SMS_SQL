from typing import List, Optional, TypeVar, Type
from src.db_engine import DBEngine

T = TypeVar('T', bound='Product')


class Product:
    """Base class representing a product.

    Attributes:
        name (str): The name of the product.
        amount (int): The amount of the product.
        price (int): The price of the product.
        id (Optional[int]): The ID of the product, if available.
    """

    def __init__(self, name: str, amount: int, price: int, id: Optional[int] = None) -> None:
        self.name = name
        self.amount = amount
        self.price = price
        self.id = id

    def save(self) -> None:
        """Save a new product or update an existing product in the database."""
        raise NotImplementedError("Subclass must implement abstract method")

    def delete(self) -> None:
        """Delete a product from the database."""
        raise NotImplementedError("Subclass must implement abstract method")

    @classmethod
    def view_all(cls: Type[T]) -> List[T]:
        """View all products in the table."""
        raise NotImplementedError("Subclass must implement abstract method")

    @classmethod
    def find_by_id(cls: Type[T], id: int) -> Optional[T]:
        """Find a product by ID."""
        raise NotImplementedError("Subclass must implement abstract method")

    def __str__(self) -> str:
        return f"ID: {self.id}, Name: {self.name}, Amount: {self.amount}, Price: {self.price}"


class DryStorageItem(Product):
    """Class representing a dry storage item.

    Attributes:
        name (str): The name of the item.
        amount (int): The amount of the item.
        price (int): The price of the item.
        recipe_item (bool): Whether the item is used in a recipe.
        chemical (bool): Whether the item is a chemical.
        package_type (str): The type of package the item comes in.
        id (Optional[int]): The ID of the item, if available.
    """

    def __init__(
            self,
            name: str,
            amount: int,
            price: int,
            recipe_item: bool,
            chemical: bool,
            package_type: str,
            id: Optional[int] = None
    ) -> None:
        super().__init__(name, amount, price, id)
        self.recipe_item = recipe_item
        self.chemical = chemical
        self.package_type = package_type

    def save(self) -> None:
        """Save a new dry storage item or update an existing item in the database."""
        with DBEngine() as db:
            if db.connection is None or db.cursor is None:
                print("Database connection error.")
                return

            if self.id is None:
                db.cursor.execute("""
                    INSERT INTO "Dry Storage Item" ("Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "DryStorageItemID"
                """, (self.name, self.amount, self.price, self.recipe_item, self.chemical, self.package_type))
                self.id = db.cursor.fetchone()[0]
            else:
                db.cursor.execute("""
                    UPDATE "Dry Storage Item"
                    SET "Name" = %s, "Amount" = %s, "Price" = %s, "RecipeItem" = %s, "Chemical" = %s, "PackageType" = %s
                    WHERE "DryStorageItemID" = %s
                """, (self.name, self.amount, self.price, self.recipe_item, self.chemical, self.package_type, self.id))
            db.connection.commit()

    def delete(self) -> None:
        """Delete a dry storage item from the database."""
        if self.id is not None:
            with DBEngine() as db:
                if db.connection is None or db.cursor is None:
                    print("Database connection error.")
                    return

                db.cursor.execute('DELETE FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
        else:
            print("Dry Storage Item ID is not set.")

    @classmethod
    def view_all(cls: Type['DryStorageItem']) -> List['DryStorageItem']:
        """View all dry storage items in the table."""
        with DBEngine() as db:
            if db.connection is None or db.cursor is None:
                print("Database connection error.")
                return []

            db.cursor.execute("""
                SELECT "DryStorageItemID", "Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType"
                FROM "Dry Storage Item"
            """)
            items = db.cursor.fetchall()
            return [cls(name=item[1], amount=item[2], price=item[3], recipe_item=item[4], chemical=item[5], package_type=item[6], id=item[0]) for item in items]

    @classmethod
    def find_by_id(cls: Type['DryStorageItem'], id: int) -> Optional['DryStorageItem']:
        """Find a dry storage item by ID."""
        with DBEngine() as db:
            if db.connection is None or db.cursor is None:
                print("Database connection error.")
                return None

            db.cursor.execute(
                'SELECT "DryStorageItemID", "Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType" FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s',
                (id,))
            item = db.cursor.fetchone()
            if item:
                return cls(name=item[1], amount=item[2], price=item[3], recipe_item=item[4], chemical=item[5], package_type=item[6], id=item[0])
            else:
                return None


class FoodItem(Product):
    """Class representing a food item.

    Attributes:
        name (str): The name of the item.
        amount (int): The amount of the item.
        price (int): The price of the item.
        storage_condition (str): The condition required for storing the item.
        expiry_date (str): The expiry date of the item in YYYY-MM-DD format.
        id (Optional[int]): The ID of the item, if available.
    """

    def __init__(
            self,
            name: str,
            amount: int,
            price: int,
            storage_condition: str,
            expiry_date: str,
            id: Optional[int] = None
    ) -> None:
        super().__init__(name, amount, price, id)
        self.storage_condition = storage_condition
        self.expiry_date = expiry_date

    def save(self) -> None:
        """Save a new food item or update an existing item in the database."""
        with DBEngine() as db:
            if db.connection is None or db.cursor is None:
                print("Database connection error.")
                return

            if self.id is None:
                db.cursor.execute("""
                    INSERT INTO "Food Item" ("Name", "Amount", "Price", "StorageCondition", "ExpiryDate")
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING "FoodItemID"
                """, (self.name, self.amount, self.price, self.storage_condition, self.expiry_date))
                self.id = db.cursor.fetchone()[0]
            else:
                db.cursor.execute("""
                    UPDATE "Food Item"
                    SET "Name" = %s, "Amount" = %s, "Price" = %s, "StorageCondition" = %s, "ExpiryDate" = %s
                    WHERE "FoodItemID" = %s
                """, (self.name, self.amount, self.price, self.storage_condition, self.expiry_date, self.id))
            db.connection.commit()

    def delete(self) -> None:
        """Delete a food item from the database."""
        if self.id is not None:
            with DBEngine() as db:
                if db.connection is None or db.cursor is None:
                    print("Database connection error.")
                    return

                db.cursor.execute('DELETE FROM "Food Item" WHERE "FoodItemID" = %s', (self.id,))
                db.connection.commit()
                self.id = None
        else:
            print("Food Item ID is not set.")

    @classmethod
    def view_all(cls: Type['FoodItem']) -> List['FoodItem']:
        """View all food items in the table."""
        with DBEngine() as db:
            if db.connection is None or db.cursor is None:
                print("Database connection error.")
                return []

            db.cursor.execute("""
                SELECT "FoodItemID", "Name", "Amount", "Price", "StorageCondition", "ExpiryDate"
                FROM "Food Item"
            """)
            items = db.cursor.fetchall()
            return [cls(name=item[1], amount=item[2], price=item[3], storage_condition=item[4], expiry_date=item[5], id=item[0]) for item in items]

    @classmethod
    def find_by_id(cls: Type['FoodItem'], id: int) -> Optional['FoodItem']:
        """Find a food item by ID."""
        with DBEngine() as db:
            if db.connection is None or db.cursor is None:
                print("Database connection error.")
                return None

            db.cursor.execute(
                'SELECT "FoodItemID", "Name", "Amount", "Price", "StorageCondition", "ExpiryDate" FROM "Food Item" WHERE "FoodItemID" = %s',
                (id,))
            item = db.cursor.fetchone()
            if item:
                return cls(name=item[1], amount=item[2], price=item[3], storage_condition=item[4], expiry_date=item[5], id=item[0])
            else:
                return None


def manage_items_menu() -> None:
    """Item management menu with options for Dry Storage and Food Items."""
    while True:
        print("\nItem Management")
        print("1. Manage Dry Storage Items")
        print("2. Manage Food Items")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            manage_dry_storage_items()
        elif choice == '2':
            manage_food_items()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")


def manage_dry_storage_items() -> None:
    """Manage Dry Storage Items with CRUD operations."""
    while True:
        print("\nDry Storage Item Management")
        print("1. Add Dry Storage Item")
        print("2. Edit Dry Storage Item")
        print("3. Delete Dry Storage Item")
        print("4. View All Dry Storage Items")
        print("5. Back")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_dry_storage_item()
        elif choice == '2':
            edit_dry_storage_item()
        elif choice == '3':
            delete_dry_storage_item()
        elif choice == '4':
            view_all_dry_storage_items()
        elif choice == '5':
            break
        else:
            print("Invalid choice, please select between 1 and 5.")


def manage_food_items() -> None:
    """Manage Food Items with CRUD operations."""
    while True:
        print("\nFood Item Management")
        print("1. Add Food Item")
        print("2. Edit Food Item")
        print("3. Delete Food Item")
        print("4. View All Food Items")
        print("5. Back")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_food_item()
        elif choice == '2':
            edit_food_item()
        elif choice == '3':
            delete_food_item()
        elif choice == '4':
            view_all_food_items()
        elif choice == '5':
            break
        else:
            print("Invalid choice, please select between 1 and 5.")


def add_dry_storage_item() -> None:
    """Prompt for and add a new dry storage item."""
    name = input("Enter item name: ")
    amount = int(input("Enter amount: "))
    price = int(input("Enter price: "))
    recipe_item = input("Is it a recipe item (yes/no)? ").strip().lower() == 'yes'
    chemical = input("Is it a chemical (yes/no)? ").strip().lower() == 'yes'
    package_type = input("Enter package type: ")
    item = DryStorageItem(name, amount, price, recipe_item, chemical, package_type)
    item.save()
    print("Dry storage item added successfully.")


def edit_dry_storage_item() -> None:
    """Prompt for ID and new data to edit an existing dry storage item."""
    id = int(input("Enter the ID of the item to edit: "))
    item = DryStorageItem.find_by_id(id)
    if item:
        name = input(f"Enter new name (current: {item.name}): ") or item.name
        amount = int(input(f"Enter new amount (current: {item.amount}): ") or item.amount)
        price = int(input(f"Enter new price (current: {item.price}): ") or item.price)
        recipe_item = input(f"Is it a recipe item (current: {item.recipe_item})? (yes/no): ").strip().lower() == 'yes'
        chemical = input(f"Is it a chemical (current: {item.chemical})? (yes/no): ").strip().lower() == 'yes'
        package_type = input(f"Enter new package type (current: {item.package_type}): ") or item.package_type
        item.name = name
        item.amount = amount
        item.price = price
        item.recipe_item = recipe_item
        item.chemical = chemical
        item.package_type = package_type
        item.save()
        print("Dry storage item updated successfully.")
    else:
        print("Item not found.")


def delete_dry_storage_item() -> None:
    """Prompt for ID and delete an existing dry storage item."""
    id = int(input("Enter the ID of the item to delete: "))
    item = DryStorageItem.find_by_id(id)
    if item:
        item.delete()
        print("Dry storage item deleted successfully.")
    else:
        print("Item not found.")


def view_all_dry_storage_items() -> None:
    """View all dry storage items."""
    items = DryStorageItem.view_all()
    for item in items:
        print(item)


def add_food_item() -> None:
    """Prompt for and add a new food item."""
    name = input("Enter item name: ")
    amount = int(input("Enter amount: "))
    price = int(input("Enter price: "))
    storage_condition = input("Enter storage condition: ")
    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
    item = FoodItem(name, amount, price, storage_condition, expiry_date)
    item.save()
    print("Food item added successfully.")


def edit_food_item() -> None:
    """Prompt for ID and new data to edit an existing food item."""
    id = int(input("Enter the ID of the item to edit: "))
    item = FoodItem.find_by_id(id)
    if item:
        name = input(f"Enter new name (current: {item.name}): ") or item.name
        amount = int(input(f"Enter new amount (current: {item.amount}): ") or item.amount)
        price = int(input(f"Enter new price (current: {item.price}): ") or item.price)
        storage_condition = input(f"Enter new storage condition (current: {item.storage_condition}): ") or item.storage_condition
        expiry_date = input(f"Enter new expiry date (current: {item.expiry_date}): ") or item.expiry_date
        item.name = name
        item.amount = amount
        item.price = price
        item.storage_condition = storage_condition
        item.expiry_date = expiry_date
        item.save()
        print("Food item updated successfully.")
    else:
        print("Item not found.")


def delete_food_item() -> None:
    """Prompt for ID and delete an existing food item."""
    id = int(input("Enter the ID of the item to delete: "))
    item = FoodItem.find_by_id(id)
    if item:
        item.delete()
        print("Food item deleted successfully.")
    else:
        print("Item not found.")


def view_all_food_items() -> None:
    """View all food items."""
    items = FoodItem.view_all()
    for item in items:
        print(item)
