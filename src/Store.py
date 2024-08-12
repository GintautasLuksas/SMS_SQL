import psycopg2
from src.db_engine import DBEngine
from Person import Worker, Manager, StoreManager

class Store:
    def __init__(self, store_name: str, worker_id: int = None, manager_id: int = None, store_manager_id: int = None):
        self.store_name = store_name
        self.worker_id = worker_id
        self.manager_id = manager_id
        self.store_manager_id = store_manager_id
        self.stock = []

    def save(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Store (store_name, worker_id, manager_id, store_manager_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (self.store_name, self.worker_id, self.manager_id, self.store_manager_id))
                self.id = cursor.fetchone()[0]
                db.connection.commit()

    def add_product(self, product_id: int, product_type: str):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if product_type == 'Food':
                    cursor.execute("""
                        INSERT INTO StoreFoodProducts (store_id, product_id)
                        VALUES (%s, %s)
                    """, (self.id, product_id))
                elif product_type == 'DryStorage':
                    cursor.execute("""
                        INSERT INTO StoreDryProduct (store_id, product_id)
                        VALUES (%s, %s)
                    """, (self.id, product_id))
                db.connection.commit()

    def remove_product(self, product_id: int, product_type: str):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if product_type == 'Food':
                    cursor.execute("""
                        DELETE FROM StoreFoodProducts
                        WHERE store_id = %s AND product_id = %s
                    """, (self.id, product_id))
                elif product_type == 'DryStorage':
                    cursor.execute("""
                        DELETE FROM StoreDryProduct
                        WHERE store_id = %s AND product_id = %s
                    """, (self.id, product_id))
                db.connection.commit()

    def add_employee(self, employee: object):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if isinstance(employee, Worker):
                    self.worker_id = employee.id
                    cursor.execute("""
                        UPDATE Store
                        SET worker_id = %s
                        WHERE id = %s
                    """, (self.worker_id, self.id))
                elif isinstance(employee, Manager):
                    self.manager_id = employee.id
                    cursor.execute("""
                        UPDATE Store
                        SET manager_id = %s
                        WHERE id = %s
                    """, (self.manager_id, self.id))
                elif isinstance(employee, StoreManager):
                    self.store_manager_id = employee.id
                    cursor.execute("""
                        UPDATE Store
                        SET store_manager_id = %s
                        WHERE id = %s
                    """, (self.store_manager_id, self.id))
                db.connection.commit()

    def remove_employee(self, employee_type: str):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                if employee_type == 'Worker':
                    cursor.execute("""
                        UPDATE Store
                        SET worker_id = NULL
                        WHERE id = %s
                    """, (self.id,))
                elif employee_type == 'Manager':
                    cursor.execute("""
                        UPDATE Store
                        SET manager_id = NULL
                        WHERE id = %s
                    """, (self.id,))
                elif employee_type == 'StoreManager':
                    cursor.execute("""
                        UPDATE Store
                        SET store_manager_id = NULL
                        WHERE id = %s
                    """, (self.id,))
                db.connection.commit()

    def load_stock(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT product_id, product_type
                    FROM StoreFoodProducts
                    WHERE store_id = %s
                """, (self.id,))
                food_products = cursor.fetchall()
                for product_id, _ in food_products:
                    self.stock.append((product_id, 'Food'))

                cursor.execute("""
                    SELECT product_id, product_type
                    FROM StoreDryProduct
                    WHERE store_id = %s
                """, (self.id,))
                dry_products = cursor.fetchall()
                for product_id, _ in dry_products:
                    self.stock.append((product_id, 'DryStorage'))

    def show_stock(self):
        for product_id, product_type in self.stock:
            print(f'Product ID: {product_id}, Product Type: {product_type}')
