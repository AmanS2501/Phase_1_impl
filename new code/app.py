import json
import os
from core.groq_llm import GroqLLM

DATA_FOLDER = "data"

SYSTEM_PROMPT = """
You are a helpful e-commerce assistant. For every user message, always reply ONLY in valid JSON specifying the action and required parameters.
Possible actions: show_cart, add_to_cart, remove_from_cart, search_products, get_order_status, reply.
For add_to_cart/remove_from_cart, always return product_id.
For search_products, reply with filters as a dictionary under the "filters" key (for example: "filters":{"gender":"women", "max_price":2000}).
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

def list_products():
    # Hardcoded mock catalog
    return [
        {"product_id": "p001", "name": "Men's Shoes Alpha", "price": 1500, "gender": "men"},
        {"product_id": "p002", "name": "Men's Shoes Beta", "price": 2200, "gender": "men"},
        {"product_id": "p003", "name": "Women's Shoes Alpha", "price": 1800, "gender": "women"},
        {"product_id": "p004", "name": "Phone Case", "price": 500, "gender": "unisex"},
    ]

def print_products(products):
    for p in products:
        print(f"{p['product_id']}: {p['name']} (₹{p['price']}) [{p['gender']}]")

def extract_filters(llm_response):
    # Accept both {"filters": {...}} and top-level fields like "gender" or "price_range"
    filters = llm_response.get("filters", {}).copy()
    # Handle LLM outputs like "gender", "max_price" at root
    if "gender" in llm_response:
        filters["gender"] = llm_response["gender"]
    if "max_price" in llm_response:
        filters["max_price"] = llm_response["max_price"]
    # Handle price_range as {"min":..,"max":..}
    if "price_range" in llm_response:
        maxv = llm_response["price_range"].get("max")
        if maxv is not None:
            filters["max_price"] = maxv
        minv = llm_response["price_range"].get("min")
        if minv is not None:
            filters["min_price"] = minv
    # Handle category if provided
    if "category" in llm_response:
        filters["category"] = llm_response["category"]
    return filters

def main():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    user_id = input("Enter your user_id: ").strip()
    llm = GroqLLM()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    print("Welcome! Type your requests (e.g., 'show my cart', 'add p003 to cart', 'show products for women')")

    from inputimeout import inputimeout, TimeoutOccurred

    TIMEOUT_SECONDS = 120

    while True:
        try:
            user_input = inputimeout(prompt="You: ", timeout=TIMEOUT_SECONDS)
        except TimeoutOccurred:
            print("\nSession timed out due to inactivity. Exiting.")
            break
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        llm_response = llm.generate(messages)
        # print(f"LLM (JSON): {llm_response}")
        try:
            res = json.loads(llm_response)
        except Exception as e:
            print("LLM did not return valid JSON. Aborting.")
            break

        action = res.get("action")
        all_products = list_products()

        if action == "show_cart":
            cart = load_cart(user_id)
            if not cart:
                print("Your cart is empty.")
            else:
                print("Your cart:")
                print_products(cart)

        elif action == "add_to_cart":
            product_id = res.get("product_id")
            product = next((p for p in all_products if p['product_id'] == product_id), None)
            if not product:
                print("Invalid product_id.")
            else:
                cart = load_cart(user_id)
                if any(item['product_id'] == product_id for item in cart):
                    print("Already in cart.")
                else:
                    cart.append(product)
                    save_cart(user_id, cart)
                    print(f"Added to cart: {product['name']}")

        elif action == "remove_from_cart":
            product_id = res.get("product_id")
            cart = load_cart(user_id)
            new_cart = [item for item in cart if item['product_id'] != product_id]
            save_cart(user_id, new_cart)
            if len(cart) == len(new_cart):
                print("Product not in cart.")
            else:
                print(f"Removed product {product_id} from cart.")

        elif action == "search_products":
            filters = extract_filters(res)
            filtered = all_products
            if "gender" in filters:
                filtered = [p for p in filtered if p['gender'].lower() == filters['gender'].lower()]
            if "max_price" in filters:
                filtered = [p for p in filtered if p['price'] <= int(filters['max_price'])]
            if "min_price" in filters:
                filtered = [p for p in filtered if p['price'] >= int(filters['min_price'])]
            # filter by category if used
            if "category" in filters and filters["category"] != "all":
                filtered = [p for p in filtered if filters["category"].lower() in p['name'].lower() or filters["category"].lower() in p.get("category", "").lower()]
            print("Products matching filters:")
            print_products(filtered)

        elif action == "reply":
            print(f"Bot: {res.get('message','')}")
        else:
            print("Unknown action. LLM output:", res)

        messages.append({"role": "assistant", "content": llm_response})

if __name__ == "__main__":
    main()
