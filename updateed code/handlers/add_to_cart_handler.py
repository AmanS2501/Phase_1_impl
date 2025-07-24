from utils.helpers import load_cart, save_cart

class AddToCartHandler:
    def __init__(self, user_id, fetch_products_fn):
        self.user_id = user_id
        self.fetch_products = fetch_products_fn

    def handle(self, product_id):
        if not product_id:
            print("No product_id specified.")
            return
        products = self.fetch_products({}, page=1, limit=50)
        product = next((p for p in products if p.get('id') == product_id), None)
        if not product:
            print("Invalid product_id.")
        else:
            cart = load_cart(self.user_id)
            if any(item.get('id') == product_id for item in cart):
                print("Already in cart.")
            else:
                cart.append(product)
                save_cart(self.user_id, cart)
                print(f"Added to cart: {product.get('title', '(No Name)')}")
