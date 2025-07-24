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

def print_products(products):
    if not products:
        print("(No products found.)")
        return
    for p in products:
        if not isinstance(p, dict):
            continue
        prod_id = p.get('id', 'N/A')
        name = p.get("title", "Unknown")
        price = p.get("price", "N/A")
        brand = p.get("brand", "")
        print(f"{prod_id}: {name} (₹{price})", f"[{brand}]" if brand else "")

def extract_filters(llm_response):
    filters = llm_response.get("filters", {}).copy()
    if "category" in llm_response:
        filters["category"] = llm_response["category"]
    if "max_price" in llm_response:
        filters["max_price"] = llm_response["max_price"]
    if "min_price" in llm_response:
        filters["min_price"] = llm_response["min_price"]
    if "price_range" in llm_response:
        pr = llm_response["price_range"]
        if "max" in pr:
            filters["max_price"] = pr["max"]
        if "min" in pr:
            filters["min_price"] = pr["min"]
    return filters
