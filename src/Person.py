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

