import unittest
from src.tables.worker_table import WorkerTable
from src.db_engine import DBEngine


class TestWorkerTable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.worker_table = WorkerTable()

    def setUp(self):
        # Setup the database by creating the table
        self.worker_table.create_table()

    def test_create_table(self):
        query = 'SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = \'Worker\')'
        self.worker_table.db_engine.cursor.execute(query)
        table_exists = self.worker_table.db_engine.cursor.fetchone()[0]
        self.assertTrue(table_exists)

    def test_insert_data(self):
        data = ("Petras Petrauskas", 654321987, "petras@example.com", "Lietuva", 15, 30)
        self.worker_table.insert_data(data)

        query = 'SELECT * FROM "Worker" WHERE "PhoneNumber" = %s'
        self.worker_table.db_engine.cursor.execute(query, (654321987,))
        worker = self.worker_table.db_engine.cursor.fetchone()

        self.assertIsNotNone(worker)
        self.assertEqual(worker[0], "Petras Petrauskas")  # Name
        self.assertEqual(worker[1], 654321987)            # PhoneNumber
        self.assertEqual(worker[2], "petras@example.com") # Email
        self.assertEqual(worker[3], "Lietuva")            # Country
        self.assertEqual(worker[4], 15)                   # HourlyRate
        self.assertEqual(worker[5], 30)                   # AmountWorked
        self.assertIsInstance(worker[6], int)             # WorkerID (last column)

    def test_update_data(self):
        data = ("Ona Onaitytė", 321654987, "ona@example.com", "Lietuva", 20, 40)
        self.worker_table.insert_data(data)

        query = 'SELECT "WorkerID" FROM "Worker" WHERE "PhoneNumber" = %s'
        self.worker_table.db_engine.cursor.execute(query, (321654987,))
        worker_id = self.worker_table.db_engine.cursor.fetchone()[0]

        new_values = {
            "Name": "Ona Juodkė",
            "PhoneNumber": 987654321,
            "Email": "ona.juodke@example.com",
            "Country": "Latvija",
            "HourlyRate": 25,
            "AmountWorked": 50
        }
        self.worker_table.update_data(worker_id, new_values)

        query = 'SELECT * FROM "Worker" WHERE "WorkerID" = %s'
        self.worker_table.db_engine.cursor.execute(query, (worker_id,))
        worker = self.worker_table.db_engine.cursor.fetchone()

        self.assertEqual(worker[0], "Ona Juodkė")           # Name
        self.assertEqual(worker[1], 987654321)              # PhoneNumber
        self.assertEqual(worker[2], "ona.juodke@example.com") # Email
        self.assertEqual(worker[3], "Latvija")              # Country
        self.assertEqual(worker[4], 25)                     # HourlyRate
        self.assertEqual(worker[5], 50)                     # AmountWorked
        self.assertEqual(worker[6], worker_id)              # WorkerID (last column)

    def test_delete_data(self):
        data = ("Aidas Aidas", 741852963, "aidas@example.com", "Lietuva", 18, 35)
        self.worker_table.insert_data(data)

        query = 'SELECT "WorkerID" FROM "Worker" WHERE "PhoneNumber" = %s'
        self.worker_table.db_engine.cursor.execute(query, (741852963,))
        worker_id = self.worker_table.db_engine.cursor.fetchone()[0]

        self.worker_table.delete_data(worker_id)

        query = 'SELECT * FROM "Worker" WHERE "WorkerID" = %s'
        self.worker_table.db_engine.cursor.execute(query, (worker_id,))
        worker = self.worker_table.db_engine.cursor.fetchone()

        self.assertIsNone(worker)

    def test_select_all(self):
        data1 = ("Rūta Rūtaitė", 852741963, "ruta@example.com", "Lietuva", 22, 40)
        data2 = ("Dainius Dainys", 369258147, "dainius@example.com", "Estija", 30, 60)
        self.worker_table.insert_data(data1)
        self.worker_table.insert_data(data2)

        workers = self.worker_table.select_all()

        self.assertGreaterEqual(len(workers), 2)
        self.assertTrue(any(worker[0] == "Rūta Rūtaitė" for worker in workers))
        self.assertTrue(any(worker[0] == "Dainius Dainys" for worker in workers))
        self.assertTrue(any(worker[1] == 852741963 for worker in workers))
        self.assertTrue(any(worker[2] == "ruta@example.com" for worker in workers))
        self.assertTrue(any(worker[3] == "Lietuva" for worker in workers))
        self.assertTrue(any(worker[4] == 22 for worker in workers))
        self.assertTrue(any(worker[5] == 40 for worker in workers))

    @classmethod
    def tearDownClass(cls):
        # Cleanup the database if necessary
        cls.worker_table.db_engine.connection.close()


if __name__ == '__main__':
    unittest.main()
