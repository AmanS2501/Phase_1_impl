from utils.helpers import load_cart, print_products

class ShowCartHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def handle(self):
        cart = load_cart(self.user_id)
        if not cart:
            print("Your cart is empty.")
        else:
            print("Your cart:")
            print_products(cart)
