# SMS_SQL

## Project Overview

SMS_SQL is a comprehensive SQL-based system designed to manage various entities such as people, products, responsibilities, and stores within an organization. This project includes functionality for handling workers, managers, store managers, food, dry storage products, and more.

## Project Structure

The project is organized into several directories and modules:

```plaintext
SMS_SQL/
├── config/
│   └── .env                             # Environment configuration file
├── myenv/                               # Virtual environment directory (not included in the repository)
├── src/
│   ├── __init__.py
│   ├── main.py                          # Main entry point for the application
│   ├── db_engine.py                     # Database engine setup and connection management
│   ├── list_tables.py                   # Utility script to list all tables in the database
│   ├── SMS_DB/                          # Database-related scripts
│   │   ├── __init__.py
│   │   ├── create_tables.py             # Script to create database tables
│   │   └── database_management.py       # Handles database creation and management
│   ├── person/                          # Modules for personnel management
│   │   ├── __init__.py
│   │   ├── manager.py                   # Manager-specific functionalities
│   │   ├── person.py                    # Base class for Person
│   │   ├── responsibilities.py          # Manage responsibilities for personnel
│   │   ├── storemanager.py              # Store Manager-specific functionalities
│   │   └── worker.py                    # Worker-specific functionalities
│   ├── product/                         # Modules for product management
│   │   ├── __init__.py
│   │   └── product.py                   # Base class and types for products (Food, Dry Storage)
│   ├── store/                           # Modules for store operations
│   │   ├── __init__.py
│   │   ├── store.py                     # Manage store details
│   │   └── store_product.py             # Manage store products and their inventory
├── test/                                # Unit and integration tests
│   ├── test_db_engine.py                # Tests for database engine module
│   ├── test_list_tables.py              # Tests for listing database tables
│   ├── test_create_tables.py            # Tests for table creation
│   ├── test_database_management.py      # Tests for database management functionalities
│   ├── test_manager.py                  # Tests for Manager functionalities
│   ├── test_person.py                   # Tests for Person base class
│   ├── test_responsibilities.py         # Tests for managing responsibilities
│   ├── test_storemanager.py             # Tests for Store Manager functionalities
│   ├── test_worker.py                   # Tests for Worker functionalities
│   ├── test_product.py                  # Tests for product functionalities
│   ├── test_store.py                    # Tests for store management
│   └── test_store_product.py            # Tests for store product management
├── .gitignore                           # Specifies files and directories to ignore in Git
├── .pre-commit-config.yaml              # Configuration for pre-commit hooks
├── mypy.ini                             # Configuration for type checking with MyPy
├── README.md                            # Project documentation
├── requirements.txt                     # Python dependencies
└── SQL_SMS.png                          # Database schema diagram
```
### Key Directories and Files

- **`config/`**: Contains configuration files, including `.env` for storing environment variables needed for database connectivity.

- **`myenv/`**: Virtual environment directory (excluded from version control) to keep project dependencies isolated.

- **`src/`**: Main source directory with subdirectories for different modules:
  - **`SMS_DB/`**: Scripts for creating and managing database tables.
  - **`person/`**: Modules for personnel management.
  - **`product/`**: Classes for managing various product types (e.g., food, dry storage items).
  - **`store/`**: Handles store operations, including store details and inventory.

- **`test/`**: Contains test modules to ensure the functionality and reliability of the application.

#### Root Files

- **`.gitignore`**: Lists files and directories to be ignored by Git.
- **`.pre-commit-config.yaml`**: Configuration for pre-commit hooks to enforce code standards and checks.
- **`mypy.ini`**: Settings for MyPy static type checking.
- **`README.md`**: Documentation with an overview, setup instructions, and usage guidelines.
- **`requirements.txt`**: Lists Python dependencies for the project.
- **`SQL_SMS.png`**: Diagram of the database schema.

This structure helps maintain a clean and organized project layout, making it easier to navigate and manage.



## Installation

Project Installation
Follow these steps to set up and run the Store Management System (SMS_SQL) on your local machine:

Clone the Repository:

Start by cloning the repository to your local machine. Open a terminal or command prompt and run:
git clone https://github.com/GintautasLuksas/SMS_SQL.git
cd SMS_SQL

Set Up a Virtual Environment:
It is recommended to use a virtual environment to manage your project’s dependencies. To create and activate a virtual environment, run the following commands:
python -m venv myenv
Activate the virtual environment:

On Windows:
myenv\Scripts\activate

On macOS and Linux:
source myenv/bin/activate
Install the Required Dependencies:

With the virtual environment activated, install the required Python packages listed in the requirements.txt file:
pip install -r requirements.txt

Configure Environment Variables:
The project uses a .env file to manage environment variables for database connectivity. You need to create this file in the config directory:
touch config/.env

Open .env in a text editor and add your PostgreSQL database connection details:
DB_NAME=your_db_name
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
HOST=your_db_host
PORT=your_db_port
Replace your_db_name, your_db_username, your_db_password, your_db_host, and your_db_port with your actual database credentials.

Set Up the Database:
Initialize the PostgreSQL database and create the necessary tables by running the create_tables.py script:
python src/SMS_DB/create_tables.py
This script will connect to your PostgreSQL database using the credentials provided in the .env file and execute the SQL commands to set up the database schema.

Run the Application:
Now, you can start the Store Management System application:
python src/main.py
This command will launch the main program, allowing you to interact with the application through the command-line interface.

Additional Notes
Database Configuration: Ensure that your PostgreSQL database server is running and accessible with the credentials specified in the .env file.
Virtual Environment: Always activate your virtual environment before running the application or any scripts to ensure the correct dependencies are used.
Dependencies: If you add or update any Python packages, remember to update requirements.txt using pip freeze > requirements.txt and commit the changes to the repository.
