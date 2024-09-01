from typing import Optional

class Person:
    """Represents a person in the system."""

    def __init__(self, name: str, phone: int, email: str, country: str, id: Optional[int] = None) -> None:
        """Initialize a new person with the given details.

        Args:
            name (str): The name of the person.
            phone (int): The phone number of the person.
            email (str): The email address of the person.
            country (str): The country of the person.
            id (Optional[int], optional): The unique identifier for the person. Defaults to None.
        """
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.country = country

    def save(self) -> None:
        """Save a new person or update an existing person in the database."""
        raise NotImplementedError("Subclasses should implement this method.")

    def delete(self) -> None:
        """Delete a person from the database."""
        raise NotImplementedError("Subclasses should implement this method.")

    @classmethod
    def view_all(cls) -> None:
        """View all people in the table."""
        raise NotImplementedError("Subclasses should implement this method.")

    def __str__(self) -> str:
        """Return a string representation of the person.

        Returns:
            str: A string describing the person.
        """
        return f"ID: {self.id}, Name: {self.name}, Phone: {self.phone}, Email: {self.email}, Country: {self.country}"
