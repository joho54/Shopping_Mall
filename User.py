import string
from Product import Product
from OutputSystem import OutputSystem
from datetime import datetime



output_system = OutputSystem()

class User:
    def __init__(self):
        self._user_id = None
        self._password = None
        self._name = None
        self._email = None
        self._cart = None
        self._money = None
        self._point = None
        self.orders = [] # transactions
        ##### optional info
        self._sex = None
        self._birthday = None
        self._nickname = None
        self._interested_category = None
    
    def update_info(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, f'_{key}'):  
                setattr(self, f'_{key}', value)
            elif hasattr(self, key):  
                setattr(self, key, value)
            else:
                print(f"{key} is not a valid attribute of User")

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        value = value.lower()
        if value not in ['male', 'female', 'other', None]:
            raise ValueError("Sex must be 'Male', 'Female', 'Other', or None")
        self._sex = value

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        date_tuple = value.split('-')
        if len(date_tuple) != 3 or len(date_tuple[0]) != 4 or len(date_tuple[1]) != 2 or len(date_tuple[2]) != 2:
            raise ValueError("Invalid Format. Format ex: 1999-09-09")
        date_object = datetime.strptime(value, "%Y-%m-%d")
        self._birthday = date_object

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if not isinstance(value, str) and value is not None:
            raise ValueError("Nickname must be a string or None")
        self._nickname = value

    @property
    def interested_category(self):
        return self._interested_category

    @interested_category.setter
    def interested_category(self, value):
        if not isinstance(value, str) and value is not None:
            raise ValueError("Interested categories must be a String or None")
        self._interested_category = value
    
    @property
    def point(self):
        return self._point
    
    @point.setter
    def point(self, value):
        self._point = value
        
    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, value):
        self._money = value
        
    @property
    def cart(self):
        return self._cart
    
    @cart.setter
    def cart(self, value):
        self._cart = value
        
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        self._user_id = value
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
           # only alphabet | only digits | too short      
        if value.isalpha() or value.isdigit() or len(value) < 8:
            raise ValueError("This is not a valid Password.")
        self._pw = value
    
    @password.getter
    def password(self):
        return self._pw
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value.isalpha():
            raise ValueError("This is not a valid name.") 
        self._name = value
    
    @name.getter
    def name(self):
        return self._name
    
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("This is not a valid email address.")
        self._email = value
    
    def place_order(self, order):
        self.orders.append(order)

    def get_order_history(self):
        return self.orders
        
    
class Cart:
    def __init__(self) -> None:
        self._user = None
        self._cart_list = None # dict {product : quantitys}
        
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise ValueError("This is not a valid User.")
        self._user = value

    @property
    def cart_list(self):
        return self._cart_list

    @cart_list.setter
    def cart_list(self, value):
        if type(value) != dict:
            raise ValueError("This is not a valid List")
        self._cart_list = value
        
        
    def add_product(self, product: Product, quantity2buy: int):
        self.cart_list[product] = quantity2buy
        
    def display_cart(self):
        output = '\n'
        display_map = {}
        output += output_system.str_format("Product Name") 
        output += output_system.str_format("Price") 
        output += output_system.str_format("Total Quantity") 
        output += output_system.str_format("Total Price") +'\n'
        output += output_system.str_format("-"*18)
        output += output_system.str_format("-"*18)
        output += output_system.str_format("-"*18)
        output += output_system.str_format("-"*18) +'\n'
        all_price = 0
        all_quantity = 0
        for idx, product in enumerate(self.cart_list, 1):
            total_price = product.price * self.cart_list[product]
            output += output_system.str_format(str(idx) + ": " + product.name)
            output += output_system.str_format(str(product.price))
            output += output_system.str_format(str(self.cart_list[product]))
            output += output_system.str_format(str(total_price)) +'\n'
            all_price += total_price
            all_quantity += self.cart_list[product]
            display_map[idx] = product.product_id
        output += f'Total Products Quantity: {all_quantity}' + '\n'
        output += f'Total Products Price: {all_price}' + '\n'
        print(output)
        return display_map
        
    
class UserManager:
    def __init__(self):
        self.users = {} # user_id : User
        self._account_DB = {} # user_id : pw
        
    
    @property
    def account_DB(self):
        return self._account_DB

    @account_DB.setter
    def account_DB(self, account_info):
        print("account db setter")
        id = account_info.get('id')
        pw = account_info.get('pw')
        if id is not None and pw is not None:
            self._account_DB[id] = pw
        self._account_DB[id] = pw
        
        
    def check_member(self, id, pw):        
        """check member using id, pw

        Args:
            id (str): input id
            pw (str): input pw

        Returns:
            bool: checking result
        """
        get_pw = self._account_DB.get(id)
        return get_pw == pw 

    def get_user(self, user_id):
        """get user by id

        Args:
            user_id (id): _description_

        Returns:
            _type_: _description_
        """
        return self.users.get(user_id, None)
    
    def add_user(self, user: User) -> bool:
        """add user

        Args:
            user (User): User instance

        Returns:
            bool: True if added. False for failure.
        """
        if user.user_id not in self.users.keys():
            self.users[user.user_id] = user
            # update data base using setter
            self.account_DB[user.user_id] = user.password
            return True
        return False

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            del self.account_DB[user_id]
            return True
        return False


    def get_all_users(self):
        return list(self.users.values())
    
    def display_info(self, user):
        output = '\n'
        info_items = [
            ('My ID: ', user.user_id),
            ('My Money: ', user.money),
            ('My Point: ', user.point),
            ('1. My Name: ', user.name),
            ('2. My email: ', user.email),
            ('3. Password: ', "****")  
        ]

        for label, value in info_items:
            output += output_system.str_format(label)
            output += output_system.str_format(value) + '\n'
        
        output += output_system.str_format('-', True) 
        output += output_system.str_format('-', True) + '\n'

        print(output)
        
    def display_optional_info(self, user: User):
        display_map = {}
        optional_list = [user.sex, user.birthday, user.nickname, user.interested_category]
        optional_names = ["Sex", "Birthday", "NickName", "Interested Category"]
        optional_attri = ["sex", "birthday", "nickname", "interested_category"]
        output = '\n'
        for idx, (name, option, attri) in enumerate(zip(optional_names, optional_list, optional_attri), 1):
            output += output_system.str_format(str(idx) + '. ')
            output += output_system.str_format(name)
            output += output_system.str_format(option) + '\n'
            display_map[idx] = attri
        print(output)
        return display_map # key: idx, val: option itself
            
        
    def disaplay_orders(self, user: User, transaction_manager):
        output = '\n'
        output += output_system.str_format('Idx / Product ') 
        output += output_system.str_format('Date / Quantity') 
        output += output_system.str_format('Order ID / Price') 
        output += output_system.str_format('Total Cost') + '\n'
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) 
        output += output_system.str_format(' ', True) + '\n'
        for idx, order in enumerate(user.orders, 1):
            output += output_system.str_format(idx) 
            output += output_system.str_format(order.transaction_date) 
            output += output_system.str_format(order.transaction_id) + '\n'
            for product in order.cart_list:
                name = product.name
                quantity = order.cart_list[product]
                each_price = product.price
                output += output_system.str_format(name) 
                output += output_system.str_format(quantity) 
                
                output += output_system.str_format(each_price) + '\n'
            total_price = transaction_manager.get_total_price(order.cart_list)
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(' ', True) 
            output += output_system.str_format(total_price) + '\n' 
        print(output)