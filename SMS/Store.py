from Person import Worker, Manager, StoreManager
class Store:
    def __init__(self, store_name: str, worker: list, managers: list, store_manager: str):
        self.store_name = store_name
        self.workers = worker
        self.managers = managers
        self.store_manager = store_manager
        self.stock = []

    def show_people(self):
        print("In this store are working:")

        print("\nWorkers:")
        if isinstance(self.workers, list):
            for worker in self.workers:
                worker.personal_info()
                worker.contact_info()
                worker.display_rate()
                worker.display_amount_worked()
                worker.display_salary()
        else:
            self.workers.personal_info()
            self.workers.contact_info()
            self.workers.display_rate()
            self.workers.display_amount_worked()
            self.workers.display_salary()

        print("\nManagers:")
        if isinstance(self.managers, list):
            for manager in self.managers:
                manager.mgr_info()
                manager.display_salary()
        else:
            self.managers.mgr_info()
            self.managers.display_salary()

        print("\nStore Manager:")
        self.store_manager.mgr_info()
        self.store_manager._MGRsalary()
        self.store_manager._MGRcash()



    def load_item_list(self, filename: str):
        with open(filename, 'r') as file:
            for line in file:
                item_details = line.strip().split(',')
                if len(item_details) == 4:
                    name, price, amount, item_code = item_details
                    self.stock.append({
                        'name': name,
                        'price': price,
                        'amount': amount,
                        'item_code': item_code
                    })

    def remove_item_list(self):
        self.stock = []
        with open('product_list.txt', 'w') as file:
            file.truncate()

    def add_worker(self, worker):
        self.workers.append(worker)

    def add_manager(self, manager):
        self.managers.append(manager)

    def set_store_manager(self, store_manager):
        self.store_manager = store_manager
