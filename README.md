# SMS_SQL

## Project Overview

SMS_SQL is a comprehensive SQL-based system designed to manage various entities such as people, products, responsibilities, and stores within an organization. This project includes functionality for handling workers, managers, store managers, food, dry storage products, and more.

## Project Structure

The project is organized into several directories and modules:

```plaintext
SMS_SQL/
├── config/
│   └── .env
├── myenv/
│   └── [virtual environment files]
├── src/
│   ├── __init__.py
│   ├── base_table.py
│   ├── db_engine.py
│   ├── list_tables.py
│   ├── main.py
│   └── tables/
│       ├── __init__.py
│       ├── dry_storage_table.py
│       ├── food_table.py
│       ├── manager_table.py
│       ├── manager_responsibilities_table.py
│       ├── responsibilities_table.py
│       ├── sm_responsibilities_table.py
│       ├── store_table.py
│       ├── store_manager_table.py
│       ├── store_dry_product_table.py
│       ├── store_food_product_table.py
│       └── worker_table.py
├── test/
│   ├── test_db_engine.py
│   ├── test_list_table.py
│   ├── test_dry_storage_table.py
│   ├── test_food_table.py
│   ├── test_manager_table.py
│   ├── test_manager_responsibilities_table.py
│   ├── test_responsibilities_table.py
│   ├── test_sm_responsibilities_table.py
│   ├── test_store_table.py
│   ├── test_store_manager_table.py
│   ├── test_store_dry_product_table.py
│   ├── test_store_food_product_table.py
│   └── test_worker_table.py
├── .gitignore
├── README.md
└── requirements.txt
```


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
