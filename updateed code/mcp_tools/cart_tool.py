import os
import json

DATA_FOLDER = "data"

def load_cart(user_id):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_cart(user_id, cart):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
    with open(path, "w") as f:
        json.dump(cart, f, indent=2)

def show_cart(user_id):
    return load_cart(user_id)

def add_to_cart(user_id, product):
    cart = load_cart(user_id)
    prod_id = product.get('id')
    if any(item.get('id') == prod_id for item in cart):
        return {"status": "already_in_cart"}
    cart.append(product)
    save_cart(user_id, cart)
    return {"status": "added", "product": product}

def remove_from_cart(user_id, product_id):
    cart = load_cart(user_id)
    new_cart = [item for item in cart if item.get('id') != product_id]
    save_cart(user_id, new_cart)
    status = "removed" if len(cart) > len(new_cart) else "not_found"
    return {"status": status}
