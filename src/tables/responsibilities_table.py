from src.base_table import BaseTable

class ResponsibilitiesTable(BaseTable):
    def __init__(self):
        columns = {
            'ResponsibilityID': 'INTEGER PRIMARY KEY',
            'ResponsibilityName': 'VARCHAR'
        }
        super().__init__("Responsibilities", columns)
