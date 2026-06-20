from Data import Basket_Of_Products
from Basket_Action import Basket_Action

class Remove_Product_From_Basket(Basket_Action):                       # Remove product from basket (Polymorphism)
    def check_Product(self, product_name):
        if product_name in Basket_Of_Products:
            del Basket_Of_Products[product_name]
            return True
        return False

    def action(self): pass
