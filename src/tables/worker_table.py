from src.db_engine import DBEngine

class WorkerTable:
    def __init__(self):
        self.db_engine = DBEngine()
        self.table_name = "Worker"

    def insert_data(self, data):
        """Insert data into the Worker table."""
        query = """
            INSERT INTO Worker (Name, PhoneNumber, Email, Country, HourlyRate, AmountWorked)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            with self.db_engine.connection.cursor() as cursor:
                cursor.execute(query, data)
                self.db_engine.connection.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
            self.db_engine.connection.rollback()

    def update_data(self, worker_id, new_values):
        """Update data in the Worker table based on worker ID."""
        set_clause = ', '.join(f"{key} = %s" for key in new_values.keys())
        values = list(new_values.values()) + [worker_id]
        query = f"UPDATE Worker SET {set_clause} WHERE WorkerID = %s"
        try:
            with self.db_engine.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.db_engine.connection.commit()
        except Exception as e:
            print(f"Error updating data: {e}")
            self.db_engine.connection.rollback()

    def delete_data(self, worker_id):
        """Delete data from the Worker table based on worker ID."""
        query = "DELETE FROM Worker WHERE WorkerID = %s"
        try:
            with self.db_engine.connection.cursor() as cursor:
                cursor.execute(query, (worker_id,))
                self.db_engine.connection.commit()
        except Exception as e:
            print(f"Error deleting data: {e}")
            self.db_engine.connection.rollback()

    def select_all(self):
        """Retrieve all data from the Worker table."""
        query = "SELECT * FROM Worker"
        try:
            with self.db_engine.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []
