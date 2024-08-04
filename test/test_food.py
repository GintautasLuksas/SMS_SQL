import unittest
from datetime import date
from src.tables.food_table import FoodTable

class TestFoodTable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.food_table = FoodTable()

    def setUp(self):
        # Ensure the table is created before each test
        self.food_table.create_table()

    def test_create_table(self):
        query = 'SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = \'Food\')'
        self.food_table.db_engine.cursor.execute(query)
        table_exists = self.food_table.db_engine.cursor.fetchone()[0]
        self.assertTrue(table_exists)

    def test_insert_data(self):
        data = ("Apples", 100, 50, "Cool and Dry", date(2024, 12, 31))
        self.food_table.insert_data(data)

        query = 'SELECT * FROM "Food" WHERE "Name" = %s'
        self.food_table.db_engine.cursor.execute(query, ("Apples",))
        food = self.food_table.db_engine.cursor.fetchone()

        self.assertIsNotNone(food)
        self.assertEqual(food[0], "Apples")                # Name (first column)
        self.assertEqual(food[1], 100)                     # Amount (second column)
        self.assertEqual(food[2], 50)                      # Price (third column)
        self.assertEqual(food[3], "Cool and Dry")          # StorageCondition (fourth column)
        self.assertEqual(food[4], date(2024, 12, 31))      # ExpiryDate (fifth column)
        self.assertIsInstance(food[5], int)                # FoodID (sixth column)

    def test_update_data(self):
        data = ("Oranges", 200, 75, "Cool and Dry", date(2024, 11, 30))
        self.food_table.insert_data(data)

        query = 'SELECT "FoodID" FROM "Food" WHERE "Name" = %s'
        self.food_table.db_engine.cursor.execute(query, ("Oranges",))
        food_id = self.food_table.db_engine.cursor.fetchone()[0]

        new_values = {
            "Name": "Oranges Updated",
            "Amount": 150,
            "Price": 80,
            "StorageCondition": "Cool and Dark",
            "ExpiryDate": date(2025, 1, 15)
        }
        self.food_table.update_data(food_id, new_values)

        query = 'SELECT * FROM "Food" WHERE "FoodID" = %s'
        self.food_table.db_engine.cursor.execute(query, (food_id,))
        food = self.food_table.db_engine.cursor.fetchone()

        self.assertEqual(food[0], "Oranges Updated")       # Name (first column)
        self.assertEqual(food[1], 150)                     # Amount (second column)
        self.assertEqual(food[2], 80)                      # Price (third column)
        self.assertEqual(food[3], "Cool and Dark")         # StorageCondition (fourth column)
        self.assertEqual(food[4], date(2025, 1, 15))       # ExpiryDate (fifth column)
        self.assertEqual(food[5], food_id)                 # FoodID (sixth column)

    def test_delete_data(self):
        data = ("Bananas", 120, 45, "Room Temperature", date(2024, 10, 10))
        self.food_table.insert_data(data)

        query = 'SELECT "FoodID" FROM "Food" WHERE "Name" = %s'
        self.food_table.db_engine.cursor.execute(query, ("Bananas",))
        food_id = self.food_table.db_engine.cursor.fetchone()[0]

        self.food_table.delete_data(food_id)

        query = 'SELECT * FROM "Food" WHERE "FoodID" = %s'
        self.food_table.db_engine.cursor.execute(query, (food_id,))
        food = self.food_table.db_engine.cursor.fetchone()

        self.assertIsNone(food)

    def test_select_all(self):
        data1 = ("Grapes", 80, 60, "Cool and Dry", date(2024, 9, 30))
        data2 = ("Pineapples", 50, 90, "Cool and Dry", date(2024, 8, 20))
        self.food_table.insert_data(data1)
        self.food_table.insert_data(data2)

        foods = self.food_table.select_all()

        self.assertGreaterEqual(len(foods), 2)
        self.assertTrue(any(food[0] == "Grapes" for food in foods))       # Check Name (first column)
        self.assertTrue(any(food[0] == "Pineapples" for food in foods))   # Check Name (first column)
        self.assertTrue(any(food[1] == 80 for food in foods))             # Check Amount (second column)
        self.assertTrue(any(food[2] == 60 for food in foods))             # Check Price (third column)
        self.assertTrue(any(food[3] == "Cool and Dry" for food in foods)) # Check StorageCondition (fourth column)
        self.assertTrue(any(food[4] == date(2024, 9, 30) for food in foods)) # Check ExpiryDate (fifth column)

    @classmethod
    def tearDownClass(cls):
        cls.food_table.db_engine.connection.close()

if __name__ == '__main__':
    unittest.main()
