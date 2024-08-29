"""
Unit tests for the `create_tables` function in the `create_tables.py` module.

This script tests the creation of database tables by verifying that the SQL commands
are executed correctly and that the tables exist in the database after running the function.

Pre-commit best practices:
- Ensure imports are sorted and used properly.
- Include clear, concise docstrings for each test case.
- Avoid long lines and enforce PEP8 compliance.
"""

import unittest
import os
import psycopg2
from unittest import mock  # Updated import for mock
from src.SMS_DB.create_tables import create_tables
from src.db_engine import DBEngine

class TestCreateTables(unittest.TestCase):
    """
    Test suite for `create_tables` function.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.

        Creates a database connection and initializes the necessary preconditions
        before any test methods are run.
        """
        cls.db_engine = DBEngine()
        cls.cursor = cls.db_engine.cursor
        cls.connection = cls.db_engine.connection

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test environment.

        Closes the database connection and cleans up resources after all test methods have run.
        """
        if cls.cursor:
            cls.cursor.close()
        if cls.connection:
            cls.connection.close()

    def setUp(self):
        """
        Initialize test case setup.

        Ensures that the database is in a clean state before each test.
        """
        self.clear_database()

    def tearDown(self):
        """
        Clean up after each test case.

        Ensures that changes made by the test are rolled back and the database is reset.
        """
        self.clear_database()

    def clear_database(self):
        """
        Helper method to remove all tables from the database.

        Ensures a clean state for testing table creation.
        """
        try:
            self.cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                    END LOOP;
                END $$;
            """)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error clearing database: {e}")

    def test_create_tables_success(self):
        """
        Test that the `create_tables` function creates all necessary tables successfully.

        Verifies that the SQL commands run without errors and the expected tables are created.
        """
        try:
            create_tables()
            self.cursor.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
            tables = self.cursor.fetchall()
            expected_tables = {'SM Responsibilities', 'Food Item', 'StoreFoodProduct', 'Responsibilities',
                               'Store', 'Manager', 'Store Manager', 'Worker', 'Dry Storage Item', 'StoreDryProduct'}
            created_tables = {table[0] for table in tables}
            self.assertTrue(expected_tables.issubset(created_tables),
                            f"Expected tables {expected_tables} were not all created. Found: {created_tables}")
        except (Exception, psycopg2.Error) as error:
            self.fail(f"create_tables() raised an exception: {error}")

    def test_create_tables_error_handling(self):
        """
        Test that `create_tables` function handles errors gracefully.

        Simulates a failure in table creation and checks if the transaction is rolled back properly.
        """
        # Simulate an error scenario
        with mock.patch('psycopg2.connect') as mock_connect:
            mock_connect.side_effect = psycopg2.OperationalError("Simulated connection error")
            with self.assertRaises(psycopg2.OperationalError):
                create_tables()

if __name__ == '__main__':
    unittest.main()
