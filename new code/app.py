# import json
# import os
# from core.groq_llm import GroqLLM

# DATA_FOLDER = "data"

# SYSTEM_PROMPT = """
# You are a helpful e-commerce assistant. For every user message, always reply ONLY in valid JSON specifying the action and required parameters.
# Possible actions: show_cart, add_to_cart, remove_from_cart, search_products, get_order_status, reply.
# For add_to_cart/remove_from_cart, always return product_id.
# For search_products, reply with filters as a dictionary under the "filters" key (for example: "filters":{"gender":"women", "max_price":2000}).
# For get_order_status, return order_id.
# If user just wants to chat, return: {"action": "reply", "message": "..."}.
# DO NOT EXPLAIN YOUR THINKING. Always reply with only the JSON.
# """

# def load_cart(user_id):
#     path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
#     if os.path.exists(path):
#         with open(path, "r") as f:
#             return json.load(f)
#     return []

# def save_cart(user_id, cart):
#     path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
#     with open(path, "w") as f:
#         json.dump(cart, f, indent=2)

# def list_products():
#     # Hardcoded mock catalog
#     return [
#         {"product_id": "p001", "name": "Men's Shoes Alpha", "price": 1500, "gender": "men"},
#         {"product_id": "p002", "name": "Men's Shoes Beta", "price": 2200, "gender": "men"},
#         {"product_id": "p003", "name": "Women's Shoes Alpha", "price": 1800, "gender": "women"},
#         {"product_id": "p004", "name": "Phone Case", "price": 500, "gender": "unisex"},
#     ]

# def print_products(products):
#     for p in products:
#         print(f"{p['product_id']}: {p['name']} (₹{p['price']}) [{p['gender']}]")

# def extract_filters(llm_response):
#     # Accept both {"filters": {...}} and top-level fields like "gender" or "price_range"
#     filters = llm_response.get("filters", {}).copy()
#     # Handle LLM outputs like "gender", "max_price" at root
#     if "gender" in llm_response:
#         filters["gender"] = llm_response["gender"]
#     if "max_price" in llm_response:
#         filters["max_price"] = llm_response["max_price"]
#     # Handle price_range as {"min":..,"max":..}
#     if "price_range" in llm_response:
#         maxv = llm_response["price_range"].get("max")
#         if maxv is not None:
#             filters["max_price"] = maxv
#         minv = llm_response["price_range"].get("min")
#         if minv is not None:
#             filters["min_price"] = minv
#     # Handle category if provided
#     if "category" in llm_response:
#         filters["category"] = llm_response["category"]
#     return filters

# def main():
#     os.makedirs(DATA_FOLDER, exist_ok=True)
#     user_id = input("Enter your user_id: ").strip()
#     llm = GroqLLM()
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT}
#     ]
#     print("Welcome! Type your requests (e.g., 'show my cart', 'add p003 to cart', 'show products for women')")

#     from inputimeout import inputimeout, TimeoutOccurred

#     TIMEOUT_SECONDS = 120

#     while True:
#         try:
#             user_input = inputimeout(prompt="You: ", timeout=TIMEOUT_SECONDS)
#         except TimeoutOccurred:
#             print("\nSession timed out due to inactivity. Exiting.")
#             break
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break
#         messages.append({"role": "user", "content": user_input})
#         llm_response = llm.generate(messages)
#         # print(f"LLM (JSON): {llm_response}")
#         try:
#             res = json.loads(llm_response)
#         except Exception as e:
#             print("LLM did not return valid JSON. Aborting.")
#             break

#         action = res.get("action")
#         all_products = list_products()

#         if action == "show_cart":
#             cart = load_cart(user_id)
#             if not cart:
#                 print("Your cart is empty.")
#             else:
#                 print("Your cart:")
#                 print_products(cart)

#         elif action == "add_to_cart":
#             product_id = res.get("product_id")
#             product = next((p for p in all_products if p['product_id'] == product_id), None)
#             if not product:
#                 print("Invalid product_id.")
#             else:
#                 cart = load_cart(user_id)
#                 if any(item['product_id'] == product_id for item in cart):
#                     print("Already in cart.")
#                 else:
#                     cart.append(product)
#                     save_cart(user_id, cart)
#                     print(f"Added to cart: {product['name']}")

#         elif action == "remove_from_cart":
#             product_id = res.get("product_id")
#             cart = load_cart(user_id)
#             new_cart = [item for item in cart if item['product_id'] != product_id]
#             save_cart(user_id, new_cart)
#             if len(cart) == len(new_cart):
#                 print("Product not in cart.")
#             else:
#                 print(f"Removed product {product_id} from cart.")

#         elif action == "search_products":
#             filters = extract_filters(res)
#             filtered = all_products
#             if "gender" in filters:
#                 filtered = [p for p in filtered if p['gender'].lower() == filters['gender'].lower()]
#             if "max_price" in filters:
#                 filtered = [p for p in filtered if p['price'] <= int(filters['max_price'])]
#             if "min_price" in filters:
#                 filtered = [p for p in filtered if p['price'] >= int(filters['min_price'])]
#             # filter by category if used
#             if "category" in filters and filters["category"] != "all":
#                 filtered = [p for p in filtered if filters["category"].lower() in p['name'].lower() or filters["category"].lower() in p.get("category", "").lower()]
#             print("Products matching filters:")
#             print_products(filtered)

#         elif action == "reply":
#             print(f"Bot: {res.get('message','')}")
#         else:
#             print("Unknown action. LLM output:", res)

#         messages.append({"role": "assistant", "content": llm_response})

# if __name__ == "__main__":
#     main()


# import json
# import os
# import requests
# from core.groq_llm import GroqLLM
# from inputimeout import inputimeout, TimeoutOccurred

# DATA_FOLDER = "data"
# ALLMART_API_URL = "https://api.allmart.fashion/api/v1/products?page=1&limit=12&sortBy=averageRating&sortOrder=desc&minPrice=0&maxPrice=1150000&inStock=false&categorySlug=electronics&recursive=true "

# SYSTEM_PROMPT = """
# You are a helpful e-commerce assistant for the Allmart platform. For every user message, always reply ONLY in valid JSON specifying the action and parameters.
# Possible actions: show_cart, add_to_cart, remove_from_cart, search_products, get_order_status, reply.
# For add_to_cart/remove_from_cart, always return id of product.
# For search_products, always return filters as a dictionary under the "filters" key, e.g. "filters":{"gender":"women", "max_price":2000, "category": "shoes"}
# For get_order_status, return order_id.
# If user just wants to chat, return: {"action": "reply", "message": "..."}.
# DO NOT EXPLAIN YOUR THINKING. Always reply with only the JSON.
# """

# TIMEOUT_SECONDS = 120  # Auto-exit after 2 min inactivity

# def load_cart(user_id):
#     path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
#     if os.path.exists(path):
#         with open(path, "r") as f:
#             return json.load(f)
#     return []

# def save_cart(user_id, cart):
#     path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
#     with open(path, "w") as f:
#         json.dump(cart, f, indent=2)

# def fetch_products(filters, page=1, limit=12):
#     params = {
#         "page": page,
#         "limit": limit,
#         "sortBy": "averageRating",
#         "sortOrder": "desc",
#         "recursive": "true",
#         "inStock": "true"
#     }
#     category = filters.get("category")
#     if category:
#         params["categorySlug"] = category
#     if filters.get("min_price") is not None:
#         params["minPrice"] = str(filters["min_price"])
#     if filters.get("max_price") is not None:
#         params["maxPrice"] = str(filters["max_price"])
#     # Additional filters (LLM may return gender, e.g., "women")
#     # API may NOT have gender filter, so we'll post-filter
#     try:
#         resp = requests.get(ALLMART_API_URL, params=params, timeout=10)
#         data = resp.json()
#     except Exception as e:
#         print("Product API error:", e)
#         return []
#     # Parse results per actual API structure
#     if isinstance(data, dict) and "data" in data and "products" in data["data"]:
#         products = data["data"]["products"]
#     else:
#         # Fallback to whatever is in "products" or "data"
#         products = data.get("products") or data.get("data") or []
#     # Post-filter by gender if needed
#     gender = filters.get("gender")
#     if gender:
#         products = [p for p in products if p.get('gender', '').lower() == gender.lower()]
#     return products

# def print_products(products):
#     if not products:
#         print("(No products found.)")
#         return
#     for p in products:
#         prod_id = p.get('product_id', p.get('_id', 'N/A'))
#         name = p.get("name", "Unknown")
#         price = p.get("price", "N/A")
#         gender = p.get("gender", "")
#         print(f"{prod_id}: {name} (₹{price})", f"[{gender}]" if gender else "")

# def extract_filters(llm_response):
#     filters = llm_response.get("filters", {}).copy()
#     # Accept gender/filter keys at top level as well
#     if "gender" in llm_response:
#         filters["gender"] = llm_response["gender"]
#     if "max_price" in llm_response:
#         filters["max_price"] = llm_response["max_price"]
#     if "min_price" in llm_response:
#         filters["min_price"] = llm_response["min_price"]
#     if "category" in llm_response:
#         filters["category"] = llm_response["category"]
#     if "price_range" in llm_response:
#         pr = llm_response["price_range"]
#         if "max" in pr:
#             filters["max_price"] = pr["max"]
#         if "min" in pr:
#             filters["min_price"] = pr["min"]
#     return filters

# def main():
#     os.makedirs(DATA_FOLDER, exist_ok=True)
#     user_id = input("Enter your user_id: ").strip()
#     llm = GroqLLM()
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT}
#     ]
#     print(
#         "Welcome! Example requests: 'show my cart', 'add <product_id> to cart', "
#         "'show products for women', 'show electronics under 5000'.\n"
#         "Type 'exit' to quit."
#     )
#     while True:
#         try:
#             user_input = inputimeout(prompt="You: ", timeout=TIMEOUT_SECONDS)
#         except TimeoutOccurred:
#             print("\nSession timed out due to inactivity. Exiting.")
#             break
#         if user_input.strip().lower() == "exit":
#             print("Goodbye!")
#             break

#         messages.append({"role": "user", "content": user_input})
#         llm_response = llm.generate(messages)
#         print(f"LLM (JSON): {llm_response}")
#         try:
#             res = json.loads(llm_response)
#         except Exception:
#             print("LLM did not return valid JSON. Please try again.")
#             continue

#         action = res.get("action")

#         if action == "show_cart":
#             cart = load_cart(user_id)
#             if not cart:
#                 print("Your cart is empty.")
#             else:
#                 print("Your cart:")
#                 print_products(cart)

#         elif action == "add_to_cart":
#             product_id = res.get("product_id")
#             if not product_id:
#                 print("No product_id specified by LLM.")
#                 continue
#             # To avoid too many/frequent API calls, fetch with default params then look up product
#             products = fetch_products({}, page=1, limit=50)
#             product = next((p for p in products if (p.get('id') == product_id or p.get('_id') == product_id)), None)
#             if not product:
#                 print("Invalid product_id.")
#             else:
#                 cart = load_cart(user_id)
#                 if any((item.get('product_id') == product_id or item.get('_id') == product_id) for item in cart):
#                     print("Already in cart.")
#                 else:
#                     cart.append(product)
#                     save_cart(user_id, cart)
#                     print(f"Added to cart: {product.get('name','(No Name)')}")

#         elif action == "remove_from_cart":
#             product_id = res.get("product_id")
#             cart = load_cart(user_id)
#             new_cart = [item for item in cart if not (item.get('product_id') == product_id or item.get('_id') == product_id)]
#             save_cart(user_id, new_cart)
#             if len(cart) == len(new_cart):
#                 print("Product not in cart.")
#             else:
#                 print(f"Removed product {product_id} from cart.")

#         elif action == "search_products":
#             filters = extract_filters(res)
#             # Default to 12 products per page
#             products = fetch_products(filters, page=1, limit=12)
#             print("Products matching filters:")
#             print_products(products)

#         elif action == "reply":
#             print(f"Bot: {res.get('message','')}")
#         else:
#             print("Unknown action. LLM output:", res)

#         messages.append({"role": "assistant", "content": llm_response})

# if __name__ == "__main__":
#     main()


import json
import os
import requests
from core.groq_llm import GroqLLM
from inputimeout import inputimeout, TimeoutOccurred

DATA_FOLDER = "data"
ALLMART_API_URL = "https://api.allmart.fashion/api/v1/products"
TIMEOUT_SECONDS = 120

SYSTEM_PROMPT = """
You are a helpful e-commerce assistant for the Allmart platform. For every user message, always reply ONLY in valid JSON specifying the action and parameters.
Possible actions: show_cart, add_to_cart, remove_from_cart, search_products, get_order_status, reply.
For add_to_cart/remove_from_cart, always return product_id as "id".
For search_products, always return filters as a dictionary under the "filters" key, e.g. "filters":{"category": "electronics", "max_price": 40000}
For get_order_status, return order_id.
If user just wants to chat, return: {"action": "reply", "message": "..."}.
DO NOT EXPLAIN YOUR THINKING. Always reply with only the JSON.
"""

def load_cart(user_id):
    path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_cart(user_id, cart):
    path = os.path.join(DATA_FOLDER, f"cart_{user_id}.json")
    with open(path, "w") as f:
        json.dump(cart, f, indent=2)

# def fetch_products(filters, page=1, limit=12):
#     params = {
#         "page": page,
#         "limit": limit,
#         "sortBy": "averageRating",
#         "sortOrder": "desc",
#         "inStock": "true"
#     }
#     # Allow for category, min/max price in params (as per API spec / query example)
#     if "category" in filters:
#         params["categorySlug"] = filters["category"]
#     if "min_price" in filters:
#         params["minPrice"] = filters["min_price"]
#     if "max_price" in filters:
#         params["maxPrice"] = filters["max_price"]
#     try:
#         resp = requests.get(ALLMART_API_URL, params=params, timeout=10)
#         data = resp.json()
#     except Exception as e:
#         print("Product API error:", e)
#         return []
#     # New: Unnest per API: data.data is the product list
#     products = (
#         data.get("data", {}).get("data") or 
#         data.get("data", []) or 
#         data.get("products", []) or []
#     )
#     return products

def fetch_products(filters, page=1, limit=12):
    params = {
        "page": page,
        "limit": limit,
        "sortBy": "averageRating",
        "sortOrder": "desc",
        "inStock": "true"
    }
    # Only send categorySlug if category is set and is not "all"
    category = filters.get("category")
    if category and category.lower() != "all":
        params["categorySlug"] = category
    if "min_price" in filters:
        params["minPrice"] = filters["min_price"]
    if "max_price" in filters:
        params["maxPrice"] = filters["max_price"]
    try:
        resp = requests.get(ALLMART_API_URL, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        print("Product API error:", e)
        return []
    products = (
        data.get("data", {}).get("data") or 
        data.get("data", []) or 
        data.get("products", []) or []
    )
    return products


def print_products(products):
    if not products:
        print("(No products found.)")
        return
    for p in products:
        prod_id = p.get('id', 'N/A')
        name = p.get("title", "Unknown")
        price = p.get("price", "N/A")
        brand = p.get("brand", "")
        print(f"{prod_id}: {name} (₹{price})", f"[{brand}]" if brand else "")

def extract_filters(llm_response):
    filters = llm_response.get("filters", {}).copy()
    # Accept filter keys at top level as well
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

def main():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    user_id = input("Enter your user_id: ").strip()
    llm = GroqLLM()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    print(
        "Welcome! Example: 'show my cart', 'add <product_id> to cart', "
        "'show electronics under 40000'.\n"
        "Type 'exit' to quit."
    )
    while True:
        try:
            user_input = inputimeout(prompt="You: ", timeout=TIMEOUT_SECONDS)
        except TimeoutOccurred:
            print("\nSession timed out due to inactivity. Exiting.")
            break
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})
        llm_response = llm.generate(messages)
        print(f"LLM (JSON): {llm_response}")
        try:
            res = json.loads(llm_response)
        except Exception:
            print("LLM did not return valid JSON. Please try again.")
            continue

        action = res.get("action")
        if action == "show_cart":
            cart = load_cart(user_id)
            if not cart:
                print("Your cart is empty.")
            else:
                print("Your cart:")
                print_products(cart)

        elif action == "add_to_cart":
            product_id = res.get("product_id") or res.get("id")
            if not product_id:
                print("No product_id specified by LLM.")
                continue
            # fetch current popular products (first page), then match the ID
            products = fetch_products({}, page=1, limit=50)
            product = next((p for p in products if p.get('id') == product_id), None)
            if not product:
                print("Invalid product_id (not found in first 50 results).")
            else:
                cart = load_cart(user_id)
                if any(item.get('id') == product_id for item in cart):
                    print("Already in cart.")
                else:
                    cart.append(product)
                    save_cart(user_id, cart)
                    print(f"Added to cart: {product.get('title','(No Name)')}")

        elif action == "remove_from_cart":
            product_id = res.get("product_id") or res.get("id")
            cart = load_cart(user_id)
            new_cart = [item for item in cart if item.get('id') != product_id]
            save_cart(user_id, new_cart)
            if len(cart) == len(new_cart):
                print("Product not in cart.")
            else:
                print(f"Removed product {product_id} from cart.")

        elif action == "search_products":
            filters = extract_filters(res)
            # Default to 12 products per page
            products = fetch_products(filters, page=1, limit=12)
            print("Products matching filters:")
            print_products(products)

        elif action == "reply":
            print(f"Bot: {res.get('message','')}")
        else:
            print("Unknown action. LLM output:", res)

        messages.append({"role": "assistant", "content": llm_response})

if __name__ == "__main__":
    main()
