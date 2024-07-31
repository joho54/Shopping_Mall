class Promotion:
    def __init__(self, name, product, discount_rate):
        self.name = name
        self.product = product
        self.discount_rate = discount_rate  

    # i will not call this.
    def apply_discount(self, product_price):
        return product_price - (product_price * (self.discount_rate / 100))

class PromotionManager:
    def __init__(self):
        self.promotions = {}  # product : Promotion 

    def add_promotion(self, promotion):
        if promotion.product not in self.promotions:
            self.promotions[promotion.product] = promotion
            promotion.product.promotion = promotion

    def remove_promotion(self, product):
        if product in self.promotions:
            del self.promotions[product]
            product.price = product.origin_price
            product.origin_price = None
            product.promotion = None
            return True
        return False

    def get_promotion(self, product):
        return self.promotions.get(product, None)

    def apply_promotion(self, product):
        if product in self.promotions:
            promotion = self.promotions[product]
            product.origin_price = product.price
            product.price = promotion.apply_discount(product.price)
            return True
        return False

    def display_promotions(self):
        for product, promotion in self.promotions.items():
            print(f"Product ID: {product}, Discount Rate: {promotion.discount_rate}%")