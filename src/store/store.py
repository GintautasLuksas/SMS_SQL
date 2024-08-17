from src.db_engine import DBEngine

class Store:
    def __init__(self, store_name: str, store_id: int = None):
        self.store_id = store_id
        self.store_name = store_name

    def save(self):
        """Save a new store or update an existing store in the database."""
        if self.store_id is None:
            self._create_store()
        else:
            self._update_store()

    def _create_store(self):
        """Insert a new store into the database."""
        with DBEngine() as db:
            try:
                db.cursor.execute("""
                    INSERT INTO "Store" ("StoreName")
                    VALUES (%s)
                    RETURNING "StoreID"
                """, (self.store_name,))
                self.store_id = db.cursor.fetchone()[0]
                db.connection.commit()
                print(f"Store '{self.store_name}' created with ID {self.store_id}.")
            except Exception as e:
                print(f"Error creating store: {e}")

    def _update_store(self):
        """Update an existing store's information."""
        with DBEngine() as db:
            try:
                db.cursor.execute("""
                    UPDATE "Store"
                    SET "StoreName" = %s
                    WHERE "StoreID" = %s
                """, (self.store_name, self.store_id))
                db.connection.commit()
                print(f"Store ID {self.store_id} updated to '{self.store_name}'.")
            except Exception as e:
                print(f"Error updating store: {e}")

    def delete(self):
        """Delete a store from the database."""
        if self.store_id is not None:
            with DBEngine() as db:
                try:
                    db.cursor.execute('DELETE FROM "Store" WHERE "StoreID" = %s', (self.store_id,))
                    db.connection.commit()
                    print(f"Store ID {self.store_id} deleted.")
                    self.store_id = None
                except Exception as e:
                    print(f"Error deleting store: {e}")
        else:
            print("Store ID is not set.")

    @classmethod
    def view_all(cls):
        """View all stores in the table."""
        with DBEngine() as db:
            try:
                db.cursor.execute('SELECT "StoreID", "StoreName" FROM "Store"')
                return db.cursor.fetchall()
            except Exception as e:
                print(f"Error retrieving stores: {e}")

def manage_store_menu():
    """Store management menu with all options."""
    while True:
        print("\nStore Management")
        print("1. Add Store")
        print("2. Edit Store")
        print("3. Delete Store")
        print("4. View All Stores")
        print("5. Back")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_store()
        elif choice == '2':
            edit_store()
        elif choice == '3':
            delete_store()
        elif choice == '4':
            view_all_stores()
        elif choice == '5':
            break
        else:
            print("Invalid choice, please select between 1 and 5.")

def add_store():
    """Add a new store."""
    store_name = input("Enter store name: ")
    store = Store(store_name)
    store.save()

def edit_store():
    """Edit an existing store."""
    store_id = int(input("Enter the ID of the store to edit: "))
    store = Store("", store_id)
    with DBEngine() as db:
        try:
            db.cursor.execute('SELECT "StoreName" FROM "Store" WHERE "StoreID" = %s', (store_id,))
            store_data = db.cursor.fetchone()
            if store_data:
                new_name = input(f"Enter new store name (current: {store_data[0]}): ") or store_data[0]
                store.store_name = new_name
                store.save()
            else:
                print("Store not found.")
        except Exception as e:
            print(f"Error editing store: {e}")

def delete_store():
    """Delete a store."""
    store_id = int(input("Enter the ID of the store to delete: "))
    store = Store("", store_id)
    store.delete()

def view_all_stores():
    """View all stores."""
    stores = Store.view_all()
    if stores:
        print("\nStores:")
        for store in stores:
            print(f"ID: {store[0]}, Name: {store[1]}")
    else:
        print("No stores found.")
