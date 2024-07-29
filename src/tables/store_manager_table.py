from src.base_table import BaseTable

class StoreManagerTable(BaseTable):
    def __init__(self):
        columns = {
            'StoreManagerID': 'INTEGER PRIMARY KEY',
            'StoreID': 'INTEGER',
            'Name': 'VARCHAR',
            'Country': 'VARCHAR',
            'Email': 'VARCHAR',
            'PhoneNumber': 'INTEGER',
            'SMResponsibilityID': 'INTEGER',
            'MonthlySalary': 'INTEGER',
            'PettyCash': 'INTEGER'
        }
        super().__init__("Store Manager", columns)
