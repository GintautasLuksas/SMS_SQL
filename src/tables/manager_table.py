from src.base_table import BaseTable

class ManagerTable(BaseTable):
    def __init__(self):
        columns = {
            'ManagerID': 'INTEGER PRIMARY KEY',
            'Name': 'VARCHAR',
            'PhoneNumber': 'VARCHAR',
            'Country': 'VARCHAR',
            'Email': 'VARCHAR',
            'MonthlySalary': 'INTEGER',
            'MGRResponibilityID': 'INTEGER'
        }
        super().__init__("Manager", columns)
