from src.base_table import BaseTable

class FoodTable(BaseTable):
    def __init__(self):
        columns = {
            'FoodID': 'INTEGER PRIMARY KEY',
            'Name': 'VARCHAR',
            'Amount': 'INTEGER',
            'Price': 'INTEGER',
            'StorageCondition': 'VARCHAR',
            'ExpiryDate': 'DATE'
        }
        super().__init__("Food", columns)
