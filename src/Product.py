import psycopg2
from src.db_engine import DBEngine

class Product:
    def __init__(self, name: str, price: int, amount: int, item_code: int, id: int = None):
        self.id = id
        self.name = name
        self.price = price
        self.amount = amount
        self.item_code = item_code

    def save(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if self.id:
                    cursor.execute("""
                        UPDATE Product
                        SET name = %s, price = %s, amount = %s, item_code = %s
                        WHERE id = %s
                    """, (self.name, self.price, self.amount, self.item_code, self.id))
                else:
                    cursor.execute("""
                        INSERT INTO Product (name, price, amount, item_code)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                    """, (self.name, self.price, self.amount, self.item_code))
                    self.id = cursor.fetchone()[0]
                db.connection.commit()

    def delete(self):
        if self.id:
            db = DBEngine()
            with db.connection:
                with db.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Product WHERE id = %s", (self.id,))
                    db.connection.commit()

    @staticmethod
    def get_by_id(product_id):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("SELECT id, name, price, amount, item_code FROM Product WHERE id = %s", (product_id,))
                result = cursor.fetchone()
                if result:
                    return Product(*result)
                else:
                    return None

    @staticmethod
    def show_products():
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Product")
                results = cursor.fetchall()
                for row in results:
                    print(row)

class DryStorage(Product):
    def __init__(self, name: str, price: int, amount: int, item_code: int, is_recipe: bool, is_chemical: bool, package: str, id: int = None):
        super().__init__(name, price, amount, item_code, id)
        self.is_recipe = is_recipe
        self.is_chemical = is_chemical
        self.package = package

    def save(self):
        super().save()  # Save the product details first
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if self.id:
                    cursor.execute("""
                        INSERT INTO DryStorage (product_id, is_recipe, is_chemical, package)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (product_id) DO UPDATE
                        SET is_recipe = EXCLUDED.is_recipe,
                            is_chemical = EXCLUDED.is_chemical,
                            package = EXCLUDED.package
                    """, (self.id, self.is_recipe, self.is_chemical, self.package))
                db.connection.commit()

    def add_to_store(self, store_id: int):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO StoreDryProduct (store_id, product_id)
                    VALUES (%s, %s)
                """, (store_id, self.id))
                db.connection.commit()

    def remove_from_store(self, store_id: int):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM StoreDryProduct
                    WHERE store_id = %s AND product_id = %s
                """, (store_id, self.id))
                db.connection.commit()

class Food(Product):
    def __init__(self, name: str, price: int, amount: int, item_code: int, expiry_date: str, storage_conditions: str, id: int = None):
        super().__init__(name, price, amount, item_code, id)
        self.expiry_date = expiry_date
        self.storage_conditions = storage_conditions

    def save(self):
        super().save()  # Save the product details first
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if self.id:
                    cursor.execute("""
                        INSERT INTO Food (product_id, expiry_date, storage_conditions)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (product_id) DO UPDATE
                        SET expiry_date = EXCLUDED.expiry_date,
                            storage_conditions = EXCLUDED.storage_conditions
                    """, (self.id, self.expiry_date, self.storage_conditions))
                db.connection.commit()

    def add_to_store(self, store_id: int):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO StoreFoodProducts (store_id, product_id)
                    VALUES (%s, %s)
                """, (store_id, self.id))
                db.connection.commit()

    def remove_from_store(self, store_id: int):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM StoreFoodProducts
                    WHERE store_id = %s AND product_id = %s
                """, (store_id, self.id))
                db.connection.commit()
