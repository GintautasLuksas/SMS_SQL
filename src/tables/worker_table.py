from src.base_table import BaseTable

class WorkerTable(BaseTable):
    def __init__(self):
        columns = {
            'WorkerID': 'INTEGER PRIMARY KEY',
            'Name': 'VARCHAR',
            'PhoneNumber': 'INTEGER',
            'Email': 'VARCHAR',
            'Country': 'VARCHAR',
            'HourlyRate': 'INTEGER',
            'AmountWorked': 'INTEGER'
        }
        super().__init__("Worker", columns)
