from src.base_table import BaseTable

class ManagerResponsibilitiesTable(BaseTable):
    def __init__(self):
        columns = {
            'MGRResponsibilityID': 'INTEGER PRIMARY KEY',
            'ResponsibilityID': 'INTEGER',
            'ManagerID': 'INTEGER'
        }
        super().__init__("Manager Responsibilities", columns)
