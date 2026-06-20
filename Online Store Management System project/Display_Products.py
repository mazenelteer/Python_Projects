class Display_Products():                                              # Display product
    data = {
        "milk": 25,"bread": 5,"eggs": 60,"rice": 30,"sugar": 20,"salt": 3,"flour": 18,"pasta": 15,
        "noodles": 12,"cornflakes": 45,"oats": 40,"honey": 70,"jam": 35,"butter": 50,"cheese": 40,
        "cream": 30,"chicken": 120,"beef": 180,"fish": 150,"shrimp": 220,"tuna": 35,
        "salmon": 250,"apple": 35,"banana": 20,"orange": 25,"grapes": 45,"mango": 30,"pineapple": 50,
        "watermelon": 40,"potato": 10,"tomato": 12,"onion": 8,"garlic": 15,"carrot": 10,"cucumber": 9,
        "pepper": 14,"eggplant": 11,"lettuce": 10,"spinach": 8,"broccoli": 18,
        "cabbage": 12,"peas": 16,"beans": 20,"lentils": 22,"chickpeas": 24,"olive_oil": 95,
        "sunflower_oil": 55,"vinegar": 18,"soy_sauce": 35,"ketchup": 28,"mayonnaise": 32,
        "mustard": 20,"chocolate": 25,"biscuits": 15,"cake": 60,"ice_cream": 40,"chips": 12,
        "popcorn": 18,"cola": 12,"orange_juice": 20,"apple_juice": 22,"water": 5,
        "sparkling_water": 9,"energy_drink": 25,"coffee": 80,"tea": 45,"green_tea": 50,
        "sugar_free_soda": 14,"detergent": 75,"dish_soap": 30,"hand_soap": 18,"shampoo": 65,
        "toothpaste": 25,"toothbrush": 15,"paper_towels": 35,"trash_bags": 40
    }

    def display_items(self):
        for product, price in self.data.items():
            print(f"{product:<20} : {price:<3} $")