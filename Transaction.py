from User import User, UserManager
from datetime import datetime
from functools import wraps
from User import UserManager

import random

class Transaction:
    """Represents a transaction in the system.

    Attributes:
        _transaction_id (str): Unique identifier for the transaction.
        _user_id (str): Identifier for the user who is part of the transaction.
        _cart_list (dict): List of items (and their quantities) being transacted.
        _transaction_date (datetime): The date and time when the transaction was made.
    """
    def __init__(self):
        """Initializes a new instance of the Transaction class."""
        self._transaction_id = None
        self._user_id = None
        self._cart_list = None
        self._transaction_date = None
        self._seller_id = None
        
    @property
    def seller_id(self):
        return self._seller_id
    
    @seller_id.setter
    def seller_id(self, value):
        self._seller_id = value

    @property
    def transaction_id(self):
        """Gets the transaction's unique identifier."""
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value):
        """Sets the transaction's unique identifier."""
        self._transaction_id = value

    @property
    def user_id(self):
        """Gets the identifier of the user involved in the transaction."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        """Sets the identifier of the user involved in the transaction."""
        self._user_id = value

    @property
    def cart_list(self):
        """Gets the list of items being transacted."""
        return self._cart_list

    @cart_list.setter
    def cart_list(self, value):
        """Sets the list of items being transacted."""
        self._cart_list = value

    @property
    def transaction_date(self):
        """Gets the date and time when the transaction was made."""
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, value):
        """Sets the date and time when the transaction was made."""
        self._transaction_date = value
        
class TransactionManager:
    """Manages transactions within the system.

    Attributes:
        _transaction_ids (list): A list of all transaction IDs.
        _user (User): The user involved in the transaction.
    """
    def __init__(self):
        """Initializes a new instance of the TransactionManager class."""
        self._transactions = None # {transaction_id: transaction}
        self._user = None
        
    @property
    def transactions(self):
        """Gets the list of transactions."""
        return self._transactions
    
    @transactions.setter
    def transactions(self, value):
        """Sets the list of transactions."""
        self._transactions = value

    @property
    def user(self):
        """Gets the user involved in the transaction."""
        return self._user

    @user.setter
    def user(self, value):
        """Sets the user involved in the transaction.

        Raises:
            ValueError: If the value is not an instance of User.
        """
        if not isinstance(value, User):
            raise ValueError("This is a invalid User")
        self._user = value

    def get_transaction_details(self):
        """Retrieves details of the transaction.

        Returns:
            dict: A dictionary containing details of the transaction.
        """
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "cart_list": self.cart_list,
            "quantity": self.quantity,
            "transaction_date": self.transaction_date
        }
        
    def get_total_price(self, cart_list: dict):
        """Calculates the total price to pay from the cart list.

        Args:
            cart_list (dict): The cart list containing products and their quantities.

        Returns:
            float: The total price of the items in the cart list.
        """
        price = 0
        for product in cart_list:
            unit_price = product.price
            quantity = cart_list[product]
            price += unit_price * quantity
        return price

    def check_balance(func):
        """Decorator to check if the user has sufficient balance for the transaction.

        Args:
            func (function): The function to wrap.

        Returns:
            function: The wrapper function.
        """
        @wraps(func)
        def wrapper(self, user: User, cart_list: dict, user_manager, seller=None):
            total_price = self.get_total_price(cart_list)
            if user.money >= total_price:
                return func(self, user, cart_list,user_manager, seller)
            else:
                print("Insufficient balance to complete the transaction.")
                return None
        return wrapper

    @check_balance
    def do_transaction(self, user: User, cart_list: dict, user_manager, seller=None):
        """Performs a transaction for the user.

        Args:
            user (User): The user performing the transaction.
            cart_list (dict): The list of items being purchased.
        """
        new_transaction = Transaction()
        new_transaction.user_id = user.user_id
        new_transaction.cart_list = cart_list
        new_transaction.transaction_date = datetime.now()
        user_id = user.user_id 
        transaction_date_str = datetime.now().strftime("%Y%m%d%H%M%S")  
        while True:
            random_int = random.randint(100, 999)  
            transaction_id = f"{user_id}-{transaction_date_str}-{random_int}"
            if transaction_id not in self.transactions.keys():
                new_transaction.transaction_id = transaction_id
                self.transactions[transaction_id] = new_transaction
                break
        for product in cart_list:
            # deduct quantity of product
            quantity = cart_list[product]
            product.quantity -= quantity 
            if seller is not None:
                pass
            elif seller is None:
                seller_id = product.seller_id
                seller = user_manager.get_user(seller_id)
            seller.my_orders[transaction_id] = [product, quantity]
                
            
        user.orders.append(new_transaction)
        user.money -= self.get_total_price(cart_list)
        