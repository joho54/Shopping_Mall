from User import User, UserManager
from InputSystem import InputSystem
from OutputSystem import OutputSystem

input_system = InputSystem()
output_system = OutputSystem()

class Seller(User):
    def __init__(self):
        super().__init__()
        self._store_name = None
        self._my_products = None
        self._my_orders = None # {order: quantity}
    
    @property
    def my_orders(self):
        return self._my_orders
    
    @my_orders.setter
    def my_orders(self, value):
        if not isinstance(value, dict):
            raise ValueError("my_orders must be a dicts")
        self._my_orders = value
        
    @property
    def my_products(self):
        return self._my_products
    
    @my_products.setter
    def my_products(self, value):
        if not isinstance(value, list):
            raise ValueError("my_products must be a list")
        self._my_products = value
    
    @property
    def store_name(self):
        return self._store_name

    @store_name.setter
    def store_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Store name must be a non-empty string")
        self._store_name = value
        
class SellerManager(UserManager):
    def __init__(self):
        super().__init__()
        
    def disaplay_orders(self, seller: Seller, transaction_manager):
        output = '\n'
        output += output_system.str_format('Idx ') 
        output += output_system.str_format('Transaction ID') 
        output += output_system.str_format('Item Name') 
        output += output_system.str_format('Price') 
        output += output_system.str_format('Quantity') 
        output += output_system.str_format('Total Cost') + '\n'
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) + '\n'
        # .transaction_date
        # transaction_id
        # seller.my_orders = {transaction_id: [product, quantity]}
        for idx, transaction_id in enumerate(seller.my_orders, 1):
            total_price = 0
            product = seller.my_orders[transaction_id][0]
            quantity = seller.my_orders[transaction_id][1]
            print(product, quantity)
            output += output_system.str_format(idx) 
            output += output_system.str_format(transaction_id) 
            output += output_system.str_format(product.name) 
            output += output_system.str_format(product.price) 
            output += output_system.str_format(quantity) 
            total_price = product.price * quantity
            output += output_system.str_format(total_price) + '\n'
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(' ', True) + '\n'
            
        # all_price = transaction_manager.get_total_price(seller.my_orders)
        # output += output_system.str_format(all_price) + '\n' 
        print(output)
        
        
        