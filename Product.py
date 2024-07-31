from OutputSystem import OutputSystem
output_system = OutputSystem()
test_products = [
    {"product_id": 1,       "name": "Laptop",             "description": "sample description2",     "quantity": 2,   "price": 1200,       "seller_id": "aaaa","category": "Electronics"},
    {"product_id": 2,       "name": "Smartphone",         "description": "sample description3",     "quantity": 3,   "price": 999,        "seller_id": "aaaa","category": "Electronics"},
    {"product_id": 3,       "name": "Coffee Maker",       "description": "sample description4",     "quantity": 4,   "price": 250,        "seller_id": "aaaa","category": "Home Appliances"},
    {"product_id": 4,       "name": "Blender",            "description": "sample description5",     "quantity": 0,   "price": 150,        "seller_id": "aaaa","category": "Home Appliances"},
    {"product_id": 5,       "name": "Desk Lamp",          "description": "sample description6",     "quantity": 6,   "price": 89,         "seller_id": "aaaa","category": "Furniture"},
    {"product_id": 6,       "name": "Ergonomic Chair",    "description": "sample description7",     "quantity": 7,   "price": 329,        "seller_id": "aaaa","category": "Furniture"}
]

def set_test_products(test_products):
    sample = []
    for product in test_products:
        new_product = Product()
        new_product.product_id = product["product_id"]
        new_product.name = product["name"]
        new_product.category = product["category"]
        new_product.description = product["description"]
        new_product.price = product["price"]
        new_product.quantity = product["quantity"]
        new_product.seller_id = product["seller_id"]
        sample.append(new_product)
    return sample
        
        

class Product:
    def __init__(self):
        self._name = None
        self._category = None
        self._description = None
        self._product_id = None
        self._price = None
        self._quantity = None
        self._seller_id = None
        self._promotion = None
        self._origin_price = None

    @property
    def origin_price(self):
        return self._origin_price
    
    @origin_price.setter
    def origin_price(self, value):
        self._origin_price = value
        
    @property
    def promotion(self):
        return self._promotion
    
    @promotion.setter
    def promotion(self, value):
        self._promotion = value

    @property
    def seller_id(self):
        return self._seller_id
    
    @seller_id.setter
    def seller_id(self, value):
        self._seller_id = value
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        self._category = value
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value
        
    @property
    def product_id(self):
        return self._product_id
    
    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
    
    def update_price(self, new_price):
        self.price = new_price

    def update_description(self, new_description):
        self.description = new_description
        
class ProductManager:
    def __init__(self):
        ## init test products.
        self.products = set_test_products(test_products)
        self.categories = ['Electronics', 'Home Appliances', 'Furniture']

    def add_product(self, product):
        self.products.append(product)
        
    def add_category(self, category: str):
        if not category in self.categories:
            self.categories.append(category)

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    def update_product_price(self, product: Product, new_price: int):
        product.price = new_price
        

    def update_product_description(self, product: Product, new_description: str):
        product.description = new_description

    def get_product(self, product_id: int):
        for product in self.products:
            if product.product_id == product_id:
                return product
        print("log: product not found by id.")
        return None

    def get_all_products(self):
        return list(self.products.values())
    
    def display_categories(self):
        print('\n++++Categories++++')
        category_map = {}
        for display_idx, category in enumerate(self.categories, 1):
            category_map[display_idx] = category
            print(f"{display_idx}. {category}")
        return category_map
    
    # this will not directly called
    def _get_products_of_category(self, category=None):
        """Returns list of product of category

        Args:
            category (str, optional): category. None will return all products.

        Returns:
            List: list of products
        """
        result = self.products if category is None else [product for product in self.products if product.category == category] 
        return result
    
    def display_products(self, category=None):
        """display product list of product manager

        Args:
            category (str, optional): Confines category to show. Defaults to None.
        Returns:
            Dict: key map for selection
        """
        display_map = {}
        selected_products = self._get_products_of_category(category)
        line_len = 66
        output = "-"*line_len + '\n'
        product_output = ''
        price_output = ''
        idx_output = ''
        special_output = ''
        display_idx = 1
        product_idx = 0
        while product_idx < len(selected_products):
            # if quantity is not
            product = selected_products[product_idx]
            if not product.quantity:
                product_idx += 1
                continue
                
            display_map[display_idx] = product.product_id
            idx_output += output_system.str_format(str(display_idx))  
            product_output += output_system.str_format(product.name)  
            
            origin_price = str(product.origin_price) + " " + product.promotion.name  + " Sale!"if product.promotion else ' '
            special_output += output_system.str_format(origin_price)  
            price_output += output_system.str_format(str(product.price))  
            # this should produce a key for choice.
            
            # 3개의 제품이 라인업되면 출력
            if (display_idx) % 3 == 0:  # idx는 0부터 시작하므로 +1을 해줍니다.
                output += idx_output + '\n'
                output += "-"*line_len + '\n'
                output += product_output + '\n'
                output += special_output + '\n'
                output += price_output + '\n'
                output += "-"*line_len + '\n'
                idx_output = ''
                product_output = ''
                price_output = ''
                special_output = ''
            product_idx += 1
            display_idx += 1

        # print rests.
        if idx_output or product_output:
            output += idx_output + '\n'
            output += "-"*line_len + '\n'
            output += product_output + '\n'
            output += special_output + '\n'
            output += price_output + '\n'
            output += "-"*line_len + '\n'
            idx_output = ''
            product_output = ''
            price_output = ''
            special_output = ''

        print(output)  # 최종적으로 구성된 문자열을 출력
        return display_map
    
    def display_a_product(self, product: Product):
        output = ''
        output += output_system.str_format('Category') + '\n'
        output += output_system.str_format(product.category) + '\n'+ '\n'
        output += output_system.str_format('Product Name') + '\n'
        output += output_system.str_format(product.name)+ '\n'+ '\n'
        output += output_system.str_format('Price') + '\n'
        output += output_system.str_format(str(product.price))+ '\n'+ '\n'
        output += output_system.str_format('Quantity') + '\n'
        output += output_system.str_format(str(product.quantity))+ '\n'+ '\n'
        output += "| " + product.description + '\n'+ '\n'
        print(output)
    
        
    
if __name__ == "__main__":
    PM = ProductManager()
    # PM.display_products("Furniture")
    PM.display_products()
    