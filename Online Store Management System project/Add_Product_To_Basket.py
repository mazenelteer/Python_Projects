from Data import Basket_Of_Products
from Display_Products import Display_Products
from Basket_Action import Basket_Action

class Add_Product_To_Basket(Display_Products, Basket_Action):          # Add product to basket (Inheritance, Polymorphism)
    def __init__(self):
        self.Product = ""

    def check_product(self, product_name):
        if product_name in self.data:
            if product_name in Basket_Of_Products:
                Basket_Of_Products[product_name] += self.data[product_name]
            else:
                Basket_Of_Products[product_name] = self.data[product_name]
            return True
        return False

    def action(self): pass