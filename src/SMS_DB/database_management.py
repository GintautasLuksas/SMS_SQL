import os
from dotenv import load_dotenv
from typing import Optional

DB_NAME: str = 'SMS'
DB_USERNAME: Optional[str] = None
DB_PASSWORD: Optional[str] = None
HOST: str = 'localhost'
PORT: int = 5432

dotenv_path: str = os.path.join(os.path.dirname(__file__), '..', '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

DB_USERNAME = os.getenv('DB_USERNAME', DB_USERNAME)
DB_PASSWORD = os.getenv('DB_PASSWORD', DB_PASSWORD)
HOST = os.getenv('HOST', HOST)
PORT = int(os.getenv('PORT', PORT))


def write_to_env_file() -> None:
    """Write the database connection details to the .env file."""
    os.makedirs(os.path.dirname(dotenv_path), exist_ok=True)
    with open(dotenv_path, 'w') as file:
        file.write(f"DB_NAME={DB_NAME}\n")
        file.write(f"DB_USERNAME={DB_USERNAME}\n")
        file.write(f"DB_PASSWORD={DB_PASSWORD}\n")
        file.write(f"HOST={HOST}\n")
        file.write(f"PORT={PORT}\n")


def create_database_and_tables() -> None:
    """Create the database and tables if connection information is complete."""
    if not all([DB_USERNAME, DB_PASSWORD]):
        print("Connection information is incomplete.")
        return

    write_to_env_file()

    from .create_tables import create_tables
    create_tables()


def database_management_menu() -> None:
    """Display the database management menu and handle user choices."""
    global DB_USERNAME, DB_PASSWORD, HOST, PORT

    while True:
        print("\nDatabase Management Menu")
        print("1. Enter Connection Information")
        print("2. Generate Database and Tables")
        print("3. Back")

        choice: str = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            DB_NAME = 'SMS'
            DB_USERNAME = input("Enter username: ").strip()
            DB_PASSWORD = input("Enter password: ").strip()
            HOST = input(f"Enter host (default {HOST}): ").strip() or HOST
            PORT_input = input(f"Enter port (default {PORT}): ").strip()
            PORT = int(PORT_input) if PORT_input else PORT
            write_to_env_file()
            print("Connection information updated and .env file created/updated.")
        elif choice == '2':
            create_database_and_tables()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")
