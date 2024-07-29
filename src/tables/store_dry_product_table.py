from src.base_table import BaseTable

class StoreDryProductTable(BaseTable):
    def __init__(self):
        columns = {
            'DryStoreID': 'INTEGER',
            'StoreID': 'INTEGER',
            'DryStorageID': 'INTEGER'
        }
        super().__init__("StoreDryProduct", columns)
