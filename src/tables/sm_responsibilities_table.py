from src.base_table import BaseTable

class SMResponsibilitiesTable(BaseTable):
    def __init__(self):
        columns = {
            'SMResponsibilityID': 'INTEGER PRIMARY KEY',
            'ResponsibilityID': 'INTEGER',
            'StoreManagerID': 'INTEGER'
        }
        super().__init__("SM Responsibilities", columns)
