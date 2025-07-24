from utils.helpers import load_cart, save_cart

class RemoveFromCartHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def handle(self, product_id):
        cart = load_cart(self.user_id)
        new_cart = [item for item in cart if item.get('id') != product_id]
        save_cart(self.user_id, new_cart)
        if len(cart) == len(new_cart):
            print("Product not in cart.")
        else:
            print(f"Removed product {product_id} from cart.")
