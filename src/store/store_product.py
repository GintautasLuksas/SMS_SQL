from src.db_engine import DBEngine

class StoreDryProduct:
    @staticmethod
    def add(store_id: int, dry_storage_id: int):
        """Add a dry storage item to a store."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                INSERT INTO "StoreDryProduct" ("StoreID", "DryStorageID")
                VALUES (%s, %s)
            """, (store_id, dry_storage_id))
            db.connection.commit()
            print("Dry storage item added to store.")
        except Exception as e:
            print(f"Error adding dry storage item to store: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @staticmethod
    def remove(store_id: int, dry_storage_id: int):
        """Remove a dry storage item from a store."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                DELETE FROM "StoreDryProduct"
                WHERE "StoreID" = %s AND "DryStorageID" = %s
            """, (store_id, dry_storage_id))
            db.connection.commit()
            print("Dry storage item removed from store.")
        except Exception as e:
            print(f"Error removing dry storage item from store: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @staticmethod
    def view(store_id: int):
        """View dry storage items in a store."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                SELECT "DryStorageID", "Name", "Amount", "Price", "RecipeItem", "Chemical", "PackageType"
                FROM "StoreDryProduct"
                JOIN "Dry Storage Item" ON "StoreDryProduct"."DryStorageID" = "Dry Storage Item"."DryStorageItemID"
                WHERE "StoreID" = %s
            """, (store_id,))
            items = db.cursor.fetchall()
            return items
        except Exception as e:
            print(f"Error viewing dry storage items in store: {e}")
            return []
        finally:
            db.cursor.close()
            db.connection.close()

class StoreFoodProduct:
    @staticmethod
    def add(store_id: int, food_id: int):
        """Add a food item to a store."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                INSERT INTO "StoreFoodProduct" ("StoreID", "FoodID")
                VALUES (%s, %s)
            """, (store_id, food_id))
            db.connection.commit()
            print("Food item added to store.")
        except Exception as e:
            print(f"Error adding food item to store: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @staticmethod
    def remove(store_id: int, food_id: int):
        """Remove a food item from a store."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                DELETE FROM "StoreFoodProduct"
                WHERE "StoreID" = %s AND "FoodID" = %s
            """, (store_id, food_id))
            db.connection.commit()
            print("Food item removed from store.")
        except Exception as e:
            print(f"Error removing food item from store: {e}")
        finally:
            db.cursor.close()
            db.connection.close()

    @staticmethod
    def view(store_id: int):
        """View food items in a store."""
        db = DBEngine()
        try:
            db.cursor.execute("""
                SELECT "FoodID", "Name", "Amount", "Price", "StorageCondition", "ExpiryDate"
                FROM "StoreFoodProduct"
                JOIN "Food Item" ON "StoreFoodProduct"."FoodID" = "Food Item"."FoodItemID"
                WHERE "StoreID" = %s
            """, (store_id,))
            items = db.cursor.fetchall()
            return items
        except Exception as e:
            print(f"Error viewing food items in store: {e}")
            return []
        finally:
            db.cursor.close()
            db.connection.close()

def manage_store_items_menu():
    """Manage Store Items with operations to add, remove, and view items."""
    while True:
        print("\nStore Item Management")
        print("1. Manage Store Dry Products")
        print("2. Manage Store Food Products")
        print("3. Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            manage_store_dry_products()
        elif choice == '2':
            manage_store_food_products()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")

def manage_store_dry_products():
    """Manage Store Dry Products with add, remove, and view operations."""
    while True:
        print("\nStore Dry Product Management")
        print("1. Add Dry Storage Item to Store")
        print("2. Remove Dry Storage Item from Store")
        print("3. View Dry Storage Items in Store")
        print("4. Back")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            add_dry_storage_item_to_store()
        elif choice == '2':
            remove_dry_storage_item_from_store()
        elif choice == '3':
            view_dry_storage_items_in_store()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please select between 1 and 4.")

def manage_store_food_products():
    """Manage Store Food Products with add, remove, and view operations."""
    while True:
        print("\nStore Food Product Management")
        print("1. Add Food Item to Store")
        print("2. Remove Food Item from Store")
        print("3. View Food Items in Store")
        print("4. Back")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            add_food_item_to_store()
        elif choice == '2':
            remove_food_item_from_store()
        elif choice == '3':
            view_food_items_in_store()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please select between 1 and 4.")

def add_dry_storage_item_to_store():
    """Prompt user to add a dry storage item to a store."""
    store_id = int(input("Enter store ID: ").strip())
    dry_storage_id = int(input("Enter dry storage item ID: ").strip())
    StoreDryProduct.add(store_id, dry_storage_id)

def remove_dry_storage_item_from_store():
    """Prompt user to remove a dry storage item from a store."""
    store_id = int(input("Enter store ID: ").strip())
    dry_storage_id = int(input("Enter dry storage item ID: ").strip())
    StoreDryProduct.remove(store_id, dry_storage_id)

def view_dry_storage_items_in_store():
    """Prompt user to view dry storage items in a store."""
    store_id = int(input("Enter store ID: ").strip())
    items = StoreDryProduct.view(store_id)
    if items:
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Price: {item[3]}, Recipe Item: {item[4]}, Chemical: {item[5]}, Package Type: {item[6]}")
    else:
        print("No dry storage items found in this store.")

def add_food_item_to_store():
    """Prompt user to add a food item to a store."""
    store_id = int(input("Enter store ID: ").strip())
    food_id = int(input("Enter food item ID: ").strip())
    StoreFoodProduct.add(store_id, food_id)

def remove_food_item_from_store():
    """Prompt user to remove a food item from a store."""
    store_id = int(input("Enter store ID: ").strip())
    food_id = int(input("Enter food item ID: ").strip())
    StoreFoodProduct.remove(store_id, food_id)

def view_food_items_in_store():
    """Prompt user to view food items in a store."""
    store_id = int(input("Enter store ID: ").strip())
    items = StoreFoodProduct.view(store_id)
    if items:
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Price: {item[3]}, Storage Condition: {item[4]}, Expiry Date: {item[5]}")
    else:
        print("No food items found in this store.")

if __name__ == "__main__":
    manage_store_items_menu()
