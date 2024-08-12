import psycopg2
from src.db_engine import DBEngine
from src.tables.worker_table import WorkerTable
from src.tables.manager_table import ManagerTable
from src.tables.store_manager_table import StoreManagerTable
from src.tables.responsibilities_table import ResponsibilitiesTable
from src.tables.sm_responsibilities_table import SMResponsibilitiesTable

class Person:
    def __init__(self, name: str, phone: int, email: str, country: str):
        self.name = name
        self.phone = phone
        self.email = email
        self.country = country
        self.id = None  # Placeholder for database ID

    def contact_info(self):
        print(f'''
Email: {self.email}
Phone number: {self.phone}
''')

    def personal_info(self):
        print(f'''
Name: {self.name}
Country: {self.country}
''')

    def save(self):
        # Placeholder method to be overridden in subclasses
        raise NotImplementedError

class Worker(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, hourly_rate: float, amount_worked: int):
        super().__init__(name, phone, email, country)
        self.hourly_rate = hourly_rate
        self.amount_worked = amount_worked

    def display_rate(self):
        print(f'Current hourly rate of {self.name} is {self.hourly_rate}')

    def display_amount_worked(self):
        print(f'{self.name} has worked {self.amount_worked} hours.')

    def display_salary(self):
        total = self.hourly_rate * self.amount_worked
        print(f'Current salary is: {total}')

    def save(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "Worker" ("Name", "PhoneNumber", "Country", "Email", "HourlyRate", "AmountWorked")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "WorkerID"
                """, (self.name, self.phone, self.email, self.country, self.hourly_rate, self.amount_worked))
                self.id = cursor.fetchone()[0]
                db.connection.commit()

class Manager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, salary: int, responsibility: str):
        super().__init__(name, phone, email, country)
        self.salary = salary
        self.responsibility = responsibility

    def display_salary(self):
        print(f'Current salary is: {self.salary}')

    def mgr_info(self):
        print(f'''
Name: {self.name}
Email: {self.email}
Phone number: {self.phone}
Country: {self.country}
Responsible for: {self.responsibility}
''')

    def save(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "Manager" ("Name", "PhoneNumber", "Country", "Email", "Salary", "Responsibility")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING "ManagerID"
                """, (self.name, self.phone, self.email, self.country, self.salary, self.responsibility))
                self.id = cursor.fetchone()[0]
                db.connection.commit()

class StoreManager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, monthly_salary: int, store_name: str, petty_cash: int):
        super().__init__(name, phone, email, country)
        self.monthly_salary = monthly_salary
        self.store_name = store_name
        self.responsibilities = []  # List to store responsibilities
        self.petty_cash = petty_cash

    def add_task(self, task: str):
        if task not in self.responsibilities:
            self.responsibilities.append(task)
            db = DBEngine()
            sm_responsibilities_table = SMResponsibilitiesTable()
            with db.connection:
                with db.connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO "SM Responsibilities" ("StoreManagerID", "ResponsibilityName")
                        VALUES (%s, %s)
                    """, (self.id, task))
                    db.connection.commit()

    def _MGRsalary(self):
        print(f'Store manager salary: {self.monthly_salary}')

    def _MGRcash(self):
        print(f'Petty cash: {self.petty_cash} left.')

    def mgr_info(self):
        print(f'''
{self.name} is responsible for {self.store_name}.
Main responsibilities include: {", ".join(self.responsibilities)}
''')

    def _petty_expense(self, expense: int):
        self.petty_cash -= expense
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE "StoreManager"
                    SET "PettyCash" = %s
                    WHERE "StoreManagerID" = %s
                """, (self.petty_cash, self.id))
                db.connection.commit()

    def save(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "StoreManager" ("Name", "PhoneNumber", "Country", "Email", "MonthlySalary", "StoreName", "PettyCash")
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING "StoreManagerID"
                """, (self.name, self.phone, self.email, self.country, self.monthly_salary, self.store_name, self.petty_cash))
                self.id = cursor.fetchone()[0]
                db.connection.commit()

class Responsibility:
    def __init__(self, responsibility_name: str):
        self.responsibility_name = responsibility_name

    def save(self):
        db = DBEngine()
        with db.connection:
            with db.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "Responsibilities" ("ResponsibilityName")
                    VALUES (%s)
                    RETURNING "ResponsibilityID"
                """, (self.responsibility_name,))
                self.id = cursor.fetchone()[0]
                db.connection.commit()
