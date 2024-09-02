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
Key Directories and Files
config/: Contains configuration files like .env which stores environment variables required for database connectivity.

myenv/: Virtual environment directory, which should not be included in version control to keep the environment isolated.

src/: Main source directory for your application, containing subdirectories for various modules:

SMS_DB/: Handles database operations such as creating and managing tables.
person/: Contains classes and functionalities related to personnel management.
product/: Manages different types of products like food and dry storage items.
store/: Manages store-specific operations including store details and inventory.
test/: This directory includes test modules to ensure the functionality and reliability of the application components.

Root Files:

.gitignore: Specifies files and directories to ignore in Git.
.pre-commit-config.yaml: Configuration for Git pre-commit hooks to enforce coding standards and check for errors before committing changes.
mypy.ini: Configuration for static type checking using MyPy.
README.md: Documentation file that provides an overview of the project, setup instructions, and usage guidelines.
requirements.txt: Lists all Python packages required to run the project.
SQL_SMS.png: Visual representation of the database schema.
This structure provides a clear and organized layout for your project, making it easy to navigate and maintain.


## Installation

To set up the project, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    ```

2. **Navigate into the project directory:**

    ```sh
    cd SMS_SQL
    ```

3. **Create and activate a virtual environment:**

    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

4. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Configure the environment variables:**

    Ensure that the `.env` file in the `config/` directory is properly set up with the necessary environment variables.

## Usage

To run the main application, execute the `main.py` script:

```sh
python src/main.py
This will start the interactive menu-driven interface for managing different entities.

Testing
To run the tests for the project, use pytest. Ensure that your virtual environment is active and then run:

sh
Copy code
pytest
This will execute all test cases defined in the test/ directory.

Modules
src/base_table.py: Defines base functionalities for table management.
src/db_engine.py: Manages the database engine connection.
src/list_tables.py: Lists and manages various tables.
src/tables/: Contains specific table management modules:
dry_storage_table.py
food_table.py
manager_table.py
manager_responsibilities_table.py
responsibilities_table.py
sm_responsibilities_table.py
store_table.py
store_manager_table.py
store_dry_product_table.py
store_food_product_table.py
worker_table.py
