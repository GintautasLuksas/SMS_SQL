import os
from dotenv import load_dotenv

# Default connection information
DB_NAME = 'SMS'
DB_USERNAME = None
DB_PASSWORD = None
HOST = 'localhost'
PORT = 5432

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Update connection information from .env file if available
DB_USERNAME = os.getenv('DB_USERNAME', DB_USERNAME)
DB_PASSWORD = os.getenv('DB_PASSWORD', DB_PASSWORD)
HOST = os.getenv('HOST', HOST)
PORT = int(os.getenv('PORT', PORT))

def write_to_env_file():
    """
    Write the current database connection information to the .env file.

    Ensures that the .env file exists, and writes the current values of DB_NAME,
    DB_USERNAME, DB_PASSWORD, HOST, and PORT to the file. This is useful for persisting
    connection details used for database operations.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(dotenv_path), exist_ok=True)

    # Write to the .env file
    with open(dotenv_path, 'w') as file:
        file.write(f"DB_NAME={DB_NAME}\n")
        file.write(f"DB_USERNAME={DB_USERNAME}\n")
        file.write(f"DB_PASSWORD={DB_PASSWORD}\n")
        file.write(f"HOST={HOST}\n")
        file.write(f"PORT={PORT}\n")

def create_database_and_tables():
    """
    Create the database and tables.

    Checks if the required connection information is available. If it is, it writes
    the details to the .env file and imports and calls the function to create the database
    tables. This function assumes that the .env file is used to configure database connections.
    """
    # Ensure .env file is loaded and connection parameters are available
    if not all([DB_USERNAME, DB_PASSWORD]):
        print("Connection information is incomplete.")
        return

    # Update .env file
    write_to_env_file()

    # Import the create_tables function
    from .create_tables import create_tables
    create_tables()

def database_management_menu():
    """
    Display the database management menu and handle user input.

    Provides a menu-driven interface for the user to input database connection details,
    generate the database and tables, or exit the menu. Updates the .env file with new
    connection information if entered by the user.
    """
    global DB_USERNAME, DB_PASSWORD, HOST, PORT

    while True:
        print("\nDatabase Management Menu")
        print("1. Enter Connection Information")
        print("2. Generate Database and Tables")
        print("3. Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            # Ensure DB_NAME is always 'SMS'
            DB_NAME = 'SMS'
            DB_USERNAME = input("Enter username: ").strip()
            DB_PASSWORD = input("Enter password: ").strip()
            HOST = input(f"Enter host (default {HOST}): ").strip() or HOST
            PORT = input(f"Enter port (default {PORT}): ").strip() or PORT
            PORT = int(PORT)
            write_to_env_file()  # Save details to .env file
            print("Connection information updated and .env file created/updated.")
        elif choice == '2':
            create_database_and_tables()
        elif choice == '3':
            break
        else:
            print("Invalid choice, please select between 1 and 3.")
