class Product:
    def __init__(self, name: str, price: int, amount: int, item_code: int):
        self.name = name
        self.price = price
        self.amount = amount
        self.item_code = item_code


    def add_item(self):
        with open('product_list.txt', 'a') as file:
            product_details = f'Product name:{self.name},Price:{self.price}Euros ,{self.amount}Units, WRIN:{self.item_code}\n'
            file.write(product_details)

    def remove_item(self):
        try:
            with open('product_list.txt', 'r') as file:
                lines = file.readlines()

            with open('product_list.txt', 'w') as file:
                for line in lines:
                    details = line.strip().split(',')
                    if str(self.item_code) != details[3]:
                        file.write(line)
        except FileNotFoundError:
            print("The file 'product_list.txt' does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_products(self):
        with open('product_list.txt') as file:
            print(file.read())


class Dry_storage(Product):
    def __init__(self,name: str, price: int, amount: int, item_code: int, is_recipe: bool, is_chemical: bool, package: str ):
        super().__init__(name, price, amount, item_code )
        self.is_recipe = is_recipe
        self.is_chemical = is_chemical
        self.package = package

    def add_item(self):
        with open('product_list.txt', 'a') as file:
            product_details = f'Product name: {self.name}, Price:{self.price}Euros, {self.amount} Units, WRIN: {self.item_code}, Is recipe:{self.is_recipe}, Is chemical: {self.is_chemical}, Package type: {self.package}\n'
            file.write(product_details)


class Food(Product):
    def __init__(self, name: str, price: int, amount: int, item_code: int, expiry_date: str, storage_conditions: str):
        super().__init__(name, price, amount, item_code)
        self.expiry_date = expiry_date
        self.storage_condition = storage_conditions

    def add_item(self):
        with open('product_list.txt', 'a') as file:
            product_details = f'Product name: {self.name},Price: {self.price}Euros,{self.amount} Units, WRIN:{self.item_code},Expiry date: {self.expiry_date},Storage condition: {self.storage_condition}.\n'
            file.write(product_details)