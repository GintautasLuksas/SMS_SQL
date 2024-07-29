from src.base_table import BaseTable

class DryStorageTable(BaseTable):
    def __init__(self):
        columns = {
            'DryStorageID': 'INTEGER PRIMARY KEY',
            'Name': 'VARCHAR',
            'Amount': 'INTEGER',
            'Price': 'INTEGER',
            'RecipeItem': 'BOOLEAN',
            'Chemical': 'BOOLEAN',
            'PackageType': 'VARCHAR'
        }
        super().__init__("Dry Storage", columns)
