# src/product/product.py

from src.db_engine import DBEngine

class Product:
    def __init__(self, name: str, amount: int, price: int, id: int = None):
        self.name = name
        self.amount = amount
        self.price = price
        self.id = id

    def save(self):
        """Save a new product or update an existing product in the database."""
        raise NotImplementedError("Subclass must implement abstract method")

    def delete(self):
        """Delete a product from the database."""
        raise NotImplementedError("Subclass must implement abstract method")

    @classmethod
    def view_all(cls):
        """View all products in the table."""
        raise NotImplementedError("Subclass must implement abstract method")

    @classmethod
    def find_by_id(cls, id: int):
        """Find a product by ID."""
        raise NotImplementedError("Subclass must implement abstract method")

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Amount: {self.amount}, Price: {self.price}"


class DryStorageItem(Product):
    def __init__(self, name: str, amount: int, price: int, recipe_item: bool, chemical: bool, package_type: str, id: int = None):
        super().__init__(name, amount, price, id)
        self.recipe_item = recipe_item
        self.chemical = chemical
        self.package_type = package_type

    def save(self):
        """Save a new dry storage item or update an existing item in the database."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            if self.id is None:
                cursor.execute("""
                    INSERT INTO "Dry Storage Item" ("Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "DryStorageItemID"
                """, (self.name, self.amount, self.price, self.recipe_item, self.chemical, self.package_type))
                self.id = cursor.fetchone()[0]
            else:
                cursor.execute("""
                    UPDATE "Dry Storage Item"
                    SET "Name" = %s, "Amount" = %s, "Price" = %s, "RecipeItem" = %s, "Chemical" = %s, "PackageType" = %s
                    WHERE "DryStorageItemID" = %s
                """, (self.name, self.amount, self.price, self.recipe_item, self.chemical, self.package_type, self.id))
            connection.commit()
        except Exception as e:
            print(f"Error saving dry storage item: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete(self):
        """Delete a dry storage item from the database."""
        if self.id is not None:
            db = DBEngine()
            connection = db.connection
            cursor = db.cursor
            try:
                cursor.execute('DELETE FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s', (self.id,))
                connection.commit()
                self.id = None
            except Exception as e:
                print(f"Error deleting dry storage item: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            print("Dry Storage Item ID is not set.")

    @classmethod
    def view_all(cls):
        """View all dry storage items in the table."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute("""
                SELECT "DryStorageItemID", "Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType"
                FROM "Dry Storage Item"
            """)
            items = cursor.fetchall()
            return [cls(*item[1:], id=item[0]) for item in items]
        except Exception as e:
            print(f"Error retrieving dry storage items: {e}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def find_by_id(cls, id: int):
        """Find a dry storage item by ID."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute('SELECT "DryStorageItemID", "Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType" FROM "Dry Storage Item" WHERE "DryStorageItemID" = %s', (id,))
            item = cursor.fetchone()
            if item:
                return cls(*item[1:], id=item[0])
            else:
                return None
        except Exception as e:
            print(f"Error finding dry storage item: {e}")
        finally:
            cursor.close()
            connection.close()


class FoodItem(Product):
    def __init__(self, name: str, amount: int, price: int, storage_condition: str, expiry_date: str, id: int = None):
        super().__init__(name, amount, price, id)
        self.storage_condition = storage_condition
        self.expiry_date = expiry_date

    def save(self):
        """Save a new food item or update an existing item in the database."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            if self.id is None:
                cursor.execute("""
                    INSERT INTO "Food Item" ("Name", "Amount", "Price", "StorageCondition", "ExpiryDate")
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING "FoodItemID"
                """, (self.name, self.amount, self.price, self.storage_condition, self.expiry_date))
                self.id = cursor.fetchone()[0]
            else:
                cursor.execute("""
                    UPDATE "Food Item"
                    SET "Name" = %s, "Amount" = %s, "Price" = %s, "StorageCondition" = %s, "ExpiryDate" = %s
                    WHERE "FoodItemID" = %s
                """, (self.name, self.amount, self.price, self.storage_condition, self.expiry_date, self.id))
            connection.commit()
        except Exception as e:
            print(f"Error saving food item: {e}")
        finally:
            cursor.close()
            connection.close()

    def delete(self):
        """Delete a food item from the database."""
        if self.id is not None:
            db = DBEngine()
            connection = db.connection
            cursor = db.cursor
            try:
                cursor.execute('DELETE FROM "Food Item" WHERE "FoodItemID" = %s', (self.id,))
                connection.commit()
                self.id = None
            except Exception as e:
                print(f"Error deleting food item: {e}")
            finally:
                cursor.close()
                connection.close()
        else:
            print("Food Item ID is not set.")

    @classmethod
    def view_all(cls):
        """View all food items in the table."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute("""
                SELECT "FoodItemID", "Name", "Amount", "Price", "StorageCondition", "ExpiryDate"
                FROM "Food Item"
            """)
            items = cursor.fetchall()
            return [cls(*item[1:], id=item[0]) for item in items]
        except Exception as e:
            print(f"Error retrieving food items: {e}")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def find_by_id(cls, id: int):
        """Find a food item by ID."""
        db = DBEngine()
        connection = db.connection
        cursor = db.cursor
        try:
            cursor.execute('SELECT "FoodItemID", "Name", "Amount", "Price", "StorageCondition", "ExpiryDate" FROM "Food Item" WHERE "FoodItemID" = %s', (id,))
            item = cursor.fetchone()
            if item:
                return cls(*item[1:], id=item[0])
            else:
                return None
        except Exception as e:
            print(f"Error finding food item: {e}")
        finally:
            cursor.close()
            connection.close()


def manage_items_menu():
    """Item management menu with options for Dry Storage and Food Items."""
    while True:
        print("\nItem Management")
        print("1. Manage Dry Storage Items")
        print("2. Manage Food Items")
        print("3. Back")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            manage_dry_storage_items()
        elif choice == '2':
            manage_food_items()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")


def manage_dry_storage_items():
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


def manage_food_items():
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


def add_dry_storage_item():
    """Add a new dry storage item."""
    name = input("Enter name: ")
    amount = int(input("Enter amount: "))
    price = int(input("Enter price: "))
    recipe_item = input("Is it a recipe item (yes/no)? ").lower() == 'yes'
    chemical = input("Is it a chemical (yes/no)? ").lower() == 'yes'
    package_type = input("Enter package type: ")
    item = DryStorageItem(name, amount, price, recipe_item, chemical, package_type)
    item.save()
    print("Dry storage item added.")


def edit_dry_storage_item():
    """Edit an existing dry storage item."""
    id = int(input("Enter ID of the item to edit: "))
    item = DryStorageItem.find_by_id(id)
    if item:
        item.name = input(f"Enter new name (current: {item.name}): ") or item.name
        item.amount = int(input(f"Enter new amount (current: {item.amount}): ") or item.amount)
        item.price = int(input(f"Enter new price (current: {item.price}): ") or item.price)
        item.recipe_item = input(f"Is it a recipe item (current: {item.recipe_item})? (yes/no): ").lower() == 'yes'
        item.chemical = input(f"Is it a chemical (current: {item.chemical})? (yes/no): ").lower() == 'yes'
        item.package_type = input(f"Enter new package type (current: {item.package_type}): ") or item.package_type
        item.save()
        print("Dry storage item updated.")
    else:
        print("Item not found.")


def delete_dry_storage_item():
    """Delete a dry storage item."""
    id = int(input("Enter ID of the item to delete: "))
    item = DryStorageItem.find_by_id(id)
    if item:
        item.delete()
        print("Dry storage item deleted.")
    else:
        print("Item not found.")


def view_all_dry_storage_items():
    """View all dry storage items."""
    items = DryStorageItem.view_all()
    if items:
        for item in items:
            print(item)
    else:
        print("No dry storage items found.")


def add_food_item():
    """Add a new food item."""
    name = input("Enter name: ")
    amount = int(input("Enter amount: "))
    price = int(input("Enter price: "))
    storage_condition = input("Enter storage condition: ")
    expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
    item = FoodItem(name, amount, price, storage_condition, expiry_date)
    item.save()
    print("Food item added.")


def edit_food_item():
    """Edit an existing food item."""
    id = int(input("Enter ID of the item to edit: "))
    item = FoodItem.find_by_id(id)
    if item:
        item.name = input(f"Enter new name (current: {item.name}): ") or item.name
        item.amount = int(input(f"Enter new amount (current: {item.amount}): ") or item.amount)
        item.price = int(input(f"Enter new price (current: {item.price}): ") or item.price)
        item.storage_condition = input(f"Enter new storage condition (current: {item.storage_condition}): ") or item.storage_condition
        item.expiry_date = input(f"Enter new expiry date (current: {item.expiry_date}): ") or item.expiry_date
        item.save()
        print("Food item updated.")
    else:
        print("Item not found.")


def delete_food_item():
    """Delete a food item."""
    id = int(input("Enter ID of the item to delete: "))
    item = FoodItem.find_by_id(id)
    if item:
        item.delete()
        print("Food item deleted.")
    else:
        print("Item not found.")


def view_all_food_items():
    """View all food items."""
    items = FoodItem.view_all()
    if items:
        for item in items:
            print(item)
    else:
        print("No food items found.")


if __name__ == "__main__":
    manage_items_menu()
