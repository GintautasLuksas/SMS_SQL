class Person:
    def __init__(self, name: str, phone: int, email: str, country: str):
        self.name = name
        self.phone = phone
        self.email = (
            email)
        self.country = country

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

class StoreManager(Person):
    def __init__(self, name: str, phone: int, email: str, country: str, monthly_salary: int, store_name: str, responsibilities: list, petty_cash: int):
        super().__init__(name, phone, email, country)
        self.monthly_salary = monthly_salary
        self.store_name = store_name
        self.responsibilities = responsibilities
        self.petty_cash = petty_cash

    def add_task(self, task):
        if task not in self.responsibilities:
            self.responsibilities.append(task)

    def _MGRsalary(self):
        print(f'Store manager salary: {self.monthly_salary}')

    def _MGRcash(self):
        print(f'Petty cash: {self.petty_cash} left.')

    def mgr_info(self):
        print(f'''
{self.name} is responsible for {self.store_name}.
Main responsibilities include: {", ".join(self.responsibilities)}
''')
    def _petty_expense(self, expense):
        self.petty_cash = self.petty_cash - expense
