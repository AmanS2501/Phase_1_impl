# import requests
# import yaml

# with open("config/config.yaml") as f:
#     CONFIG = yaml.safe_load(f)

# class MCPClient:
#     def __init__(self):
#         self.base_url = CONFIG["mcp_api"]["base_url"]
#         self.headers = {"Authorization": f"Bearer {CONFIG['mcp_api']['api_key']}"}

#     def get_order_status(self, order_id):
#         resp = requests.get(f"{self.base_url}/orders/{order_id}", headers=self.headers)
#         return resp.json()

#     def search_products(self, filters):
#         resp = requests.get(f"{self.base_url}/products", params=filters, headers=self.headers)
#         return resp.json()

#     def modify_cart(self, user_id, product_id, action):
#         resp = requests.post(
#             f"{self.base_url}/cart",
#             json={"user_id": user_id, "product_id": product_id, "action": action},
#             headers=self.headers,
#         )
#         return resp.json()

#     def get_category_link(self, category):
#         resp = requests.get(f"{self.base_url}/categories/{category}", headers=self.headers)
#         return resp.json().get("link")



# # Mock data instead of mcp for testing purposes
# class MCPClient:
#     def __init__(self):
#         # Mock dataset
#         self.orders = {
#             "12345": {"status": "Shipped", "order_id": "12345"},
#             "54321": {"status": "Delivered", "order_id": "54321"},
#             "67890": {"status": "Pending", "order_id": "67890"},
#         }
#         self.products = [
#             {"name": "Men's Shoes Alpha", "price": 1500, "gender": "men", "product_id": "p001"},
#             {"name": "Men's Shoes Beta", "price": 2200, "gender": "men", "product_id": "p002"},
#             {"name": "Women's Shoes Alpha", "price": 1800, "gender": "women", "product_id": "p003"},
#             {"name": "Phone Case", "price": 500, "gender": "unisex", "product_id": "p004"},
#         ]
#         self.cart = []
#         self.categories = {
#             "mobile-accessories": "https://mockstore.com/categories/mobile-accessories",
#             "shoes": "https://mockstore.com/categories/shoes"
#         }

#     def get_order_status(self, order_id):
#         return self.orders.get(order_id, {})

#     def search_products(self, filters):
#         filtered = self.products
#         if "max_price" in filters:
#             filtered = [p for p in filtered if p["price"] <= filters["max_price"]]
#         if "gender" in filters:
#             filtered = [p for p in filtered if p.get("gender") == filters["gender"]]
#         return filtered

#     def modify_cart(self, user_id, product_id, action):
#         # Basic mock, cart not user-specific
#         product = next((p for p in self.products if p["product_id"] == product_id), None)
#         message = "Cart unchanged."
#         if not product:
#             return {"message": "Product not found."}
#         if action == "add":
#             self.cart.append(product)
#             message = f"Added {product['name']} to cart."
#         elif action == "remove":
#             self.cart = [item for item in self.cart if item["product_id"] != product_id]
#             message = f"Removed product {product_id} from cart."
#         return {"message": message}

#     def get_category_link(self, category):
#         return self.categories.get(category)


import json
import os

class MCPClient:
    def __init__(self, user_id):
        self.user_id = user_id
        self.products = [
            {"name": "Men's Shoes Alpha", "price": 1500, "gender": "men", "product_id": "p001"},
            {"name": "Men's Shoes Beta", "price": 2200, "gender": "men", "product_id": "p002"},
            {"name": "Women's Shoes Alpha", "price": 1800, "gender": "women", "product_id": "p003"},
            {"name": "Phone Case", "price": 500, "gender": "unisex", "product_id": "p004"},
        ]
        self.orders = {
            "12345": {"status": "Shipped", "order_id": "12345"},
            "54321": {"status": "Delivered", "order_id": "54321"},
            "67890": {"status": "Pending", "order_id": "67890"},
        }
        self.categories = {
            "mobile-accessories": "https://mockstore.com/categories/mobile-accessories",
            "shoes": "https://mockstore.com/categories/shoes"
        }
        self.cart_file = f"cart_{self.user_id}.json"
        self.cart = self.load_cart()

    def load_cart(self):
        if os.path.exists(self.cart_file):
            with open(self.cart_file, "r") as f:
                return json.load(f)
        return []

    def save_cart(self):
        with open(self.cart_file, "w") as f:
            json.dump(self.cart, f)

    def get_order_status(self, order_id):
        return self.orders.get(order_id, {})

    def search_products(self, filters):
        filtered = self.products
        if "max_price" in filters:
            filtered = [p for p in filtered if p["price"] <= filters["max_price"]]
        if "gender" in filters:
            filtered = [p for p in filtered if p.get("gender") == filters["gender"]]
        return filtered

    def modify_cart(self, product_id, action):
        product = next((p for p in self.products if p["product_id"] == product_id), None)
        if not product:
            return {"message": "Product not found."}
        if action == "add":
            if not any(x['product_id'] == product_id for x in self.cart):
                self.cart.append(product)
                self.save_cart()
                return {"message": f"Added {product['name']} to cart."}
            else:
                return {"message": "Product already in cart."}
        elif action == "remove":
            self.cart = [item for item in self.cart if item["product_id"] != product_id]
            self.save_cart()
            return {"message": f"Removed product {product_id} from cart."}
        return {"message": "Cart unchanged."}

    def get_category_link(self, category):
        return self.categories.get(category)

    def get_cart(self):
        return self.cart

    def analyze_cart(self):
        items = self.cart
        total = sum(item.get("price", 0) for item in items)
        details = [f"{item['name']} (₹{item['price']})" for item in items]
        summary = f"Cart has {len(items)} items, total ₹{total}."
        return summary, details
