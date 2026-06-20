from Data import Basket_Of_Products

class Total_Price():                                                   # Total price
    def __init__(self):
        self.Total = 0

    def calculate_Total_price(self):
        self.Total = 0
        for product, price in Basket_Of_Products.items():
            self.Total += price
        return self.Total
