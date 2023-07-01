class Calculator:

    @staticmethod
    def calculate_quantity_total_in_cart(products):
        quantity_total = 0
        for product in products:
            quantity_total += product["quantidade"]
        return quantity_total

    @staticmethod
    def calculate_price_total_in_cart(price, quantity):
        price_total = price * quantity
        return price_total
