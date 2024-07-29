from src.base_table import BaseTable

class StoreFoodProductTable(BaseTable):
    def __init__(self):
        columns = {
            'FoodStorageID': 'INTEGER',
            'StoreID': 'INTEGER',
            'FoodID': 'INTEGER'
        }
        super().__init__("StoreFoodProduct", columns)
