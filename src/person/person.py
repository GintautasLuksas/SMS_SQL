

class Person:
    def __init__(self, name: str, phone: int, email: str, country: str, id: int = None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.country = country

    def save(self):
        """Save a new person or update an existing person in the database."""
        raise NotImplementedError("Subclasses should implement this method.")

    def delete(self):
        """Delete a person from the database."""
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def view_all(cls):
        """View all people in the table."""
        raise NotImplementedError("Subclasses should implement this method.")

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Phone: {self.phone}, Email: {self.email}, Country: {self.country}"
