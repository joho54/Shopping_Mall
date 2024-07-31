from User import User, UserManager, Cart
from InputSystem import InputSystem
from Product import Product, ProductManager
from Transaction import TransactionManager, Transaction
from Seller import Seller, SellerManager
from Promotion import Promotion, PromotionManager

input_system = InputSystem()
user_manager = UserManager()
product_manager = ProductManager()
transaction_manager = TransactionManager() 
seller_manager = SellerManager()
promotion_manager = PromotionManager()

#  set transaction_ids
transaction_manager.transactions = {}

# login_page.py
def login():
    # get user id
    id = input_system.get_input("ID: ")
    pw = input_system.get_input("PW: ")
    is_member = user_manager.check_member(id, pw)
    if is_member:
        user = user_manager.get_user(id)
        transaction_manager.user = user
        if isinstance(user, Seller):
            return pass6(user)
        return pass2(user)
    else:
        print("\nInvalid user information. Please try again.")
        return pass1()

def logout():
    print("\nYou have been logged out.")
    return True

# signup_page.py
def signup():
    print("\nSign Up")
    flag_id = True
    flag_pw = True
    # while loop using flags.
    while True: 
        new_user = User()
        try:
            # get every values for Customer
            if flag_id:
                id = input_system.get_input("ID: ")
                if user_manager.get_user(id):
                    print("ID already exists.")
                    flag_id = True
                    continue
                else: flag_id = False
            new_user.user_id = id
                
            if flag_pw:
                # get another informations.
                print("\nPassword should contain one more alphabets and digits, More than 8 characters.")
                pw = input_system.get_input("PW: ")
                pw_2 = input_system.get_input("PW double check: ")
                if (pw != pw_2):
                    print("Failed Double Check.")
                    flag_pw = True
                    continue
                else: flag_pw = False
            new_user.password  = pw
            
            name = input_system.get_input("Name: ")
            new_user.name = name
            email = input_system.get_input("Email: ")
            new_user.email = email
            
        except ValueError as e:
            print(f"\nFailed to create a new user. {e}")
            return False
        
        user_manager.add_user(new_user)
        new_cart = Cart()
        new_cart.cart_list = {}
        new_cart.user = new_user
        
        # this is part for test.
        new_user.money = 10000000
        new_user.point = 10000000
        new_user.cart = new_cart
        print("Signed up successful.")
        return True

def signup_as_seller():
    print("\nSign Up as a Seller")
    flag_id = True
    flag_pw = True
    while True: 
        new_seller = Seller()
        try:
            # User ID
            if flag_id:
                id = input_system.get_input("User ID: ")
                if user_manager.get_user(id):
                    print("This ID is already taken.")
                    flag_id = True
                    continue
                else:
                    flag_id = False
                    new_seller.user_id = id
                    
            if flag_pw:
                # Password
                pw = input_system.get_input("PW: ")
                pw_2 = input_system.get_input("PW double check: ")
                if pw != pw_2:
                    print("Failed Double Check.")
                    flag_pw = True
                    continue
                else:
                    flag_pw = False
                    new_seller.password = pw

            # Name
            name = input_system.get_input("Name: ")
            new_seller.name = name

            # Email
            email = input_system.get_input("Email: ")
            new_seller.email = email

            # Store Name
            store_name = input_system.get_input("Store Name: ")
            new_seller.store_name = store_name

        except ValueError as e:
            print(f"\nFailed to create a new seller. {e}")
            return False

        # init rest infos
        new_seller.my_products = []
        new_seller.my_orders = {}
        user_manager.add_user(new_seller)  # Assuming user_manager can handle both User and Seller objects
        
        
        print("Signed up as seller successful.")
        return True

def pass1():
    while True:
        print("\nWelcome")
        top_menu = '\t|\t'.join(["1. Log in", "2. Sign up", "3. Sign up as a Seller", "4. Quit"])
        print(top_menu)
        choice = input_system.get_input_range("\nChoose your option: ", ['1', '2', '3', '4'])
        if choice == '1':
            return login()
        elif choice == '2':
            signup()
        elif choice == '3':
            signup_as_seller()
        elif choice == '4':
            print("Quiting.")
            return        
        
def pass2(user: User):
    # menu after log in. 
    category_val = None
    while True:
        print()
        top_menu = '\t|\t'.join(["a. My Page", "b. My Cart", "c. Log Out,", "d. Categories", 'e. All Products'])
        print(top_menu)
        alpha_menus = ['a', 'b', 'c', 'd', 'e']
        display_map = product_manager.display_products(category_val)
        choice = input_system.get_input_range("Choose index of product. Enter the alphabet for other Menus.: ", \
            [*tuple(map(str, display_map.keys())), *alpha_menus])
        if choice.isalpha():
            if choice == 'a':
                return pass5(user)
            elif choice == 'b':
                return pass4(user)
            elif choice == 'c':
                logout()
                return pass1()
            elif choice == 'd':
                # print categories and then give argument to display_product
                category_map = product_manager.display_categories()
                category = input_system.get_input("Enter index of the category you want to see: ", int)
                category_val = category_map.get(int(category), None)
                if category_val is None:
                    print("Warning: Category does not exists.")
                    continue
            elif choice == 'e':
                category_val = None
                continue
            else:
                print("Warning: Invalid input. please try again.")
        else:
            # else user choose a product.
            key = int(choice)
            product_id = display_map[key]
            product = product_manager.get_product(product_id)
            # call pass 3 and return
            return pass3(user, product)

def pass3(user: User, product: Product):
    # detailed product menu
    print("\n")
    product_manager.display_a_product(product)
    choice = None
    while True:
        top_menu = '\t|\t'.join(["a. Add to Cart", "b. Buy", "c. Go Back", "d. My Cart"])
        print(top_menu)
        alpha_menus = ['a', 'b', 'c','d']
        # add to cart, buy, back.
        choice = input_system.get_input_range("Choose your option: ", [*alpha_menus]) if choice is None else choice
        if choice == 'a':
            quantity = input_system.get_input("How many items you wantto add?: ", int)
            quantity = int(quantity)
            if product in user.cart.cart_list.keys():
                is_update = input_system.get_input("You already have same product in your cart. Do you want to update quantity? [y/n]: ", str)
                if is_update.lower() == 'y':
                    quantity = user.cart.cart_list[product] + quantity # update quantity
                    pass
                else:
                    choice = None
                    continue
            
            # update quantity and add
            if  quantity > product.quantity:
                print("Quantity is out of stock.\n")
                choice = 'a'
                choice = None
                continue
            user.cart.add_product(product, quantity)
            product_manager.add_category(product.category)
            choice = None
            print(f"\n{product.name} added to your cart.\n")
            
        elif choice == 'b':
            quantity = input_system.get_input("How many items you want to buy?: ", int)
            quantity = int(quantity)
            if  quantity > product.quantity:
                print("Quantity is out of stock.\n")
                choice = 'a'
                choice = None
                continue
            tmp_cart = {product: quantity}
            seller = user_manager.get_user(product.seller_id)
            transaction_manager.do_transaction(user, tmp_cart, user_manager, seller)
    
            print(f"\n{product.name} purchased.\n")
            choice = None
            return pass2(user)
            
        elif choice == 'c':
            choice = None
            return pass2(user)
        elif choice == 'd':
            choice = None
            return pass4(user)

# my cart
def pass4(user: User):
    if isinstance(user, Seller):
        print("not available menu")
        return pass6(user)
    choice = None
    while True:
        display_map = user.cart.display_cart()
        top_menu = '\t|\t'.join(["a. Check Out", "b. Select to purchase", "c. Select to remove", "d. To the Item Page", "e. Go back", "f. Clear the Cart"])
        print(top_menu)
        alpha_menus = ['a', 'b', 'c','d', 'e' , 'f']
        # add to cart, buy, back.
        choice = input_system.get_input_range("Choose your option: ", [*alpha_menus]) if choice is None else choice
        if choice == 'a':
            # first get all product list
            total_price = transaction_manager.get_total_price(user.cart.cart_list)
            if user.money < total_price:
                print("Not enough money.")
            # else: do transaction
            else:
                transaction_manager.do_transaction(user, user.cart.cart_list, user_manager)
                print("Transaction success!")
            user.cart.cart_list = {}
            choice = None
            
        elif choice == 'b':
            selected_map = {}
            indices = input_system.get_input("Enter Indices of products with commas. ex) 1, 3, 4: ")
            indices = indices.split(',')
            
            # validity check.
            for idx in indices:
                idx = idx.strip()
                if not idx.isdigit():
                    print("Invalid input. Please try again")
                    continue
                idx = int(idx)
                if not idx in display_map:
                    print("Index doesn't matches. Please try again")
                    continue
                product = product_manager.get_product(display_map[idx])
                quantity = user.cart.cart_list[product]
                
                selected_map[product] = quantity
            
            print("\nYou chose Following products")
            for sel in selected_map:
                print(sel.name, selected_map[sel])
            
            total_price = transaction_manager.get_total_price(user.cart.cart_list)
            print("Price to Pay:", total_price)
                
            if user.money < total_price:
                print("Not enough money.")
            # else: do transaction
            else:
                seller = user_manager.get_user(product.seller_id)
                transaction_manager.do_transaction(user, user.cart.cart_list, user_manager, seller)
                print("Transaction success!")
                
            # delete selected_map from cart
            for key in selected_map.keys():
                user.cart.cart_list.pop(key)  
            choice = None
            
        elif choice == 'c':
            indices = input_system.get_input("Enter Indices of products with commas. ex) 1, 3, 4: ")
            indices = indices.split(',')
            
            # validity check.
            for idx in indices:
                idx = idx.strip()
                if not idx.isdigit():
                    print("Invalid input. Please try again")
                    continue
                idx = int(idx)
                if not idx in display_map:
                    print("Index doesn't matches. Please try again")
                    continue
                product = product_manager.get_product(display_map[idx])
                
                del user.cart.cart_list[product]
            choice = None
        
        elif choice == 'd':
            display_idx = input_system.get_input_range("Enter the index of item: ", tuple(map(str, display_map.keys())))
            display_idx = int(display_idx)
            product_id = display_map[display_idx]
            product = product_manager.get_product(product_id)
            return pass3(user, product)
        
        elif choice == 'e':
            choice = None
            return pass2(user)
        
        elif choice == 'f':
            user.cart.cart_list = {}
            print("Your cart has been Cleared")
            display_map = user.cart.display_cart()
            choice = None

def pass5(user: User):
    choice = None
    while True:
        user_manager.display_info(user)
        top_menu = '\t|\t'.join(["a. Change My Info", "b. Retister Optional Info", "c. Delete My Account", "d. My Orders", "e. Go Back"])
        print(top_menu)
        alpha_menus = ['a', 'b', 'c','d', 'e']

        choice = input_system.get_input_range("Choose your option: ", [*alpha_menus]) if choice is None else choice
        if choice == 'a':
            
            idx = input_system.get_input_range("Choose Index you want to change: ", ['1', '2', '3'])
            if idx == '1':
                name = input_system.get_input("Enter you name to change: ", str)
                try:
                    user.name = name
                except ValueError as e:
                    print(f"\nFailed to change. {e}")
                    
            elif idx == '2':
                email = input_system.get_input("Enter email to change: ")
                try:
                    user.email = email
                except ValueError as e:
                    print(f"\nFailed to change. {e}")
                pass
            elif idx == '3':
                # user verification
                check_pw = input_system.get_input("Enter current password: ")
                if check_pw != user.password:
                    print("Incorrect Password")
                    continue
                password = input_system.get_input("Enter password to change: ")
                password_double = input_system.get_input("Enter password to double check: ")
                if password != password_double:
                    print("Double check failed.")
                    continue
                try:
                    user.password = password
                    user_manager.account_DB[user.user_id] = user.password
                except ValueError as e:
                    print(f"\nFailed to change. {e}")
            choice = None
            
        elif choice == 'b':
            # register optional info
            top_menu = '\t|\t'.join(["a. Go back"])
            print(top_menu)
            alpha_menus = ['a']
            display_map = user_manager.display_optional_info(user) # key: idx, val: optioanl info itself
            option = input_system.get_input_range("Enter the index you want to set. Enter alphabet for other options: ", [*tuple(map(str, display_map.keys())), 'a'])
            if option == 'a':
                choice = None
                continue
            option = int(option)
            new_info = input_system.get_input("Enter New info: ")
            try: 
                setattr(user, display_map[option], new_info)
            except ValueError as e:
                print(f"\nFailed to change. {e}")
                continue
            print("Info changed Successfuly")
            choice = None
        elif choice == 'c':
            confirm = input_system.get_input_range("Are you sure you want to delete your account? [y/n]: ", ['y', 'n'])
            if confirm == 'y':
                password = input_system.get_input("Enter password: ")
                if password != user.password:
                    print("Incorrect Password")
                else: 
                    is_removed =  user_manager.remove_user(user.user_id)
                    if is_removed:
                        print("Account Deleted")
                        pass1()
                        return
                    else:
                        print("Remove Failed")
                        
            choice = None
            
        elif choice == 'd':
            user_manager.disaplay_orders(user, transaction_manager)
            choice = None
        
        elif choice == 'e':
            if isinstance(user, Seller):
                return pass6(user)
            return pass2(user)

def pass6(seller: Seller):
    # get statistics
    # create a promotion
    
    # menu after log in as a Seller 
    category_val = None
    while True:
        print()
        top_menu = '\t|\t'.join(["a. My Page", "b. Add Products", "c. Check Products,", "d. Revise Products", 'e. Check Orders', 'f. Manage Promotions', 'g. Log Out' , 'h. Category'])
        print(top_menu)
        alpha_menus = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        display_map = product_manager.display_products(category_val)
        choice = input_system.get_input_range("Choose index of product. Enter the alphabet for other Menus: ", \
            [*tuple(map(str, display_map.keys())), *alpha_menus])
        if choice.isalpha():
            if choice == 'a':
                return pass5(seller)
            
            elif choice == 'b':
                new_product = Product()
                try:
                    # Name
                    name = input_system.get_input("Enter product name: ", str)
                    new_product.name = name

                    # Category
                    category = input_system.get_input("Enter product category: ", str)
                    new_product.category = category

                    # Description
                    description = input_system.get_input("Enter product description: ", str)
                    new_product.description = description

                    # Product ID
                    product_id = input_system.get_input("Enter product ID: ", int)
                    product_id = int(product_id)
                    new_product.product_id = product_id

                    # Price
                    price = input_system.get_input("Enter product Price: ", int)
                    price = int(price)
                    new_product.price = price

                    # Quantity
                    quantity = input_system.get_input("Enter product quantity: ", int)
                    quantity = int(quantity)
                    new_product.quantity = quantity

                except ValueError as e:
                    print(f"Error adding product: {e}")
                product_manager.add_product(new_product)
                seller.my_products.append(new_product)
                
            elif choice == 'c':
                for product in seller.my_products:
                    product_manager.display_a_product(product)
                    
            elif choice == 'd':
                # revise products
                display_map = {}
                for idx, product in enumerate(seller.my_products, 1):
                    print(f'{idx}. {product.name}')
                    display_map[idx] = product
                product_idx = input_system.get_input_range("Choose Index of Product to revise: ", tuple(map(str, display_map.keys())))
                product_idx = int(product_idx)
                # get product
                product = display_map[product_idx]
                product_manager.display_a_product(product)
                revise_menu = '\t|\t'.join(["1. Category", "2. Name", "3. Description", "4. Price", "5. Quantity"])
                print(revise_menu)
                revise_idx = input_system.get_input_range("Choose option to revise: ", ['1', '2', '3', '4', '5'])
                if revise_idx == '1':
                    new_category = input_system.get_input("Enter new Category: ")
                    product.category = new_category
                    product_manager.add_category(product.category)
                elif revise_idx == '2':
                    new_name = input_system.get_input("Enter new name: ")
                    product.name = new_name
                elif revise_idx == '3':
                    new_description = input_system.get_input("Enter new description: ")
                    product.description = new_description
                elif revise_idx == '4':
                    new_price = input_system.get_input("Enter new price: ", int)
                    new_price = int(new_price)
                    product.price = new_price
                elif revise_idx == '5':
                    new_quantity = input_system.get_input("Enter new quantity: ", int)
                    new_quantity = int(new_quantity)
                    product.quantity = new_quantity
                
            elif choice == 'e':
                # check orders. 
                for product in seller.my_orders:
                    seller_manager.disaplay_orders(seller, transaction_manager)
            elif choice == 'f':
                # display seller's product name name and product list
                print('\nYour Products')
                for product in seller.my_products:
                    print(f'product id: {product.product_id}  |  product name: {product.name}')
                
                print("\nYour Promotions")
                for product in promotion_manager.promotions:
                    if product.seller_id != seller.user_id:
                        continue
                    promotion = promotion_manager.promotions[product]
                    print(f'product name: {product.name}  |  promotion name: {promotion.name}  |  promotion percantage: {promotion.discount_rate}')
                    
                promo_menu = '\t|\t'.join(["1. Create Promo", "2. Remove Promo", "3. Go back"])
                print(promo_menu)
                choice_2 = input_system.get_input_range("Choose option to revise: ", ['1', '2', '3'])
                
                if choice_2 == '1':
                    # create promo
                    product_id = input_system.get_input("Enter Product Id you want to set promotion: ", int)
                    product_id = int(product_id)
                    product = product_manager.get_product(product_id)
                    if product is not None:
                        promotion_name = input_system.get_input("Enter Promotion name: ", str)
                        promotion_rate = input_system.get_input("Enter Promotion percantage : ", int)
                        promotion_rate = int(promotion_rate)
                        promotion = Promotion(promotion_name, product, promotion_rate)
                        promotion_manager.add_promotion(promotion)
                        promotion_manager.apply_promotion(product)
                        
                elif choice_2 == '2':
                    # create promo
                    product_id = input_system.get_input("Enter Product Id you want to remove promotion: ", int)
                    product_id = int(product_id)
                    product = product_manager.get_product(product_id)
                    if product is not None:
                        promotion_manager.remove_promotion(product)
                elif choice_2 == '3':
                    choice = None
                    continue
                    
            elif choice == 'g':
                logout()
                return pass1()
            elif choice == 'h':
                category_map = product_manager.display_categories()
                category = input_system.get_input("Enter index of the category you want to see: ", int)
                category_val = category_map.get(int(category), None)
                if category_val is None:
                    print("Warning: Category does not exists.")
                    continue
            else:
                print("Warning: Invalid input. please try again.")
        else:
            # else user choose a product.
            key = int(choice)
            product_id = display_map[key]
            product = product_manager.get_product(product_id)
            # seller can not buy product. only can check.
            product_manager.display_a_product(product)
            
def main():
    pass1()
    
if __name__ == "__main__":
    ###### Test User and Seller Data.
    test_cart = Cart()
    test_user = User() ##### test user.
    test_seller = Seller() ##### test seller
    
    test_cart.cart_list = {}
    test_cart.user = test_user
    
    test_user.name = 'cho'
    test_user.user_id = 'admin'
    test_user.password = 'asdfasdf1234'
    test_user.email = 'joho43@naver.com'
    test_user.cart = test_cart
    test_user.money = 100000000
    test_user.point = 100000000.0
    
    test_seller.name = 'cho'
    test_seller.user_id = 'aaaa'
    test_seller.password = 'asdfasdf1234'
    test_seller.email = 'joho43@naver.com'
    test_seller.cart = test_cart
    test_seller.money = 100000000
    test_seller.point = 100000000.0
    test_seller.store_name = "Awesome Store"
    
    user_manager.users = {test_user.user_id : test_user, test_seller.user_id: test_seller} # user_id : User
    user_manager._account_DB = {test_user.user_id : test_user.password, test_seller.user_id: test_seller.password} # user_id : pw
    
    product1 = product_manager.get_product(1)
    product2 = product_manager.get_product(2)
    product3 = product_manager.get_product(3)
    product4 = product_manager.get_product(4)
    test_seller.my_products = [product1, product2, product3, product4]
    test_product = product_manager.products[0]
    
    test_trans = Transaction()
    test_trans.cart_list = { test_product : 1} # product itself, quantity
    test_trans.user_id = 'admin'
    test_trans.transaction_id = '234234234'
    test_trans.transaction_date = '1999-09-09'
    test_trans.seller_id = 'aaaa'
    test_seller.my_orders = {}
    transaction_manager.transactions[test_trans.transaction_id] = test_trans
    print([test_user, test_trans.cart_list, user_manager, test_seller])
    transaction_manager.do_transaction(test_user, test_trans.cart_list, user_manager, test_seller)
    
    
    main()