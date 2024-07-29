from src.base_table import BaseTable
class StoreTable(BaseTable):
    def __init__(self):
        columns = {
            'StoreID': 'INTEGER PRIMARY KEY',
            'StoreName': 'VARCHAR',
            'StoreManagerID': 'INTEGER',
            'ManagerID': 'INTEGER',
            'WorkerID': 'INTEGER',
            'FoodStorageID': 'INTEGER',
            'DryStoreID': 'INTEGER'
        }
        super().__init__("Store", columns)
