import json
import requests
from inputimeout import inputimeout, TimeoutOccurred
from core.groq_llm import GroqLLM
from prompt.system_prompt import SYSTEM_PROMPT
from utils.helpers import extract_filters
from handlers.show_cart_handler import ShowCartHandler
from handlers.add_to_cart_handler import AddToCartHandler
from handlers.remove_from_cart_handler import RemoveFromCartHandler
from handlers.search_products_handler import SearchProductsHandler
from handlers.faq_handler import FAQHandler

ALLMART_API_URL = "https://api.allmart.fashion/api/v1/products"
TIMEOUT_SECONDS = 120

def fetch_products(filters, page=1, limit=12):
    params = {
        "page": page,
        "limit": limit,
        "sortBy": "averageRating",
        "sortOrder": "desc",
        "inStock": "true"
    }
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
    products = [p for p in products if isinstance(p, dict)]
    return products

def get_user_id():
    user_id = input("Enter your user_id: ").strip()
    if not user_id:
        print("User ID cannot be empty. Please try again.")
        return get_user_id()
    return user_id

def main():
    # user_id = input("Enter your user_id: ").strip()
    llm = GroqLLM()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    # show_cart_handler = ShowCartHandler(user_id)
    # add_to_cart_handler = AddToCartHandler(user_id, fetch_products)
    # remove_from_cart_handler = RemoveFromCartHandler(user_id)
    # search_products_handler = SearchProductsHandler(fetch_products)
    # faq_handler = FAQHandler()

    print(
        "Welcome! Try typing: 'show my cart', 'add <product_id> to cart', "
        "'remove <product_id> from cart', 'show electronics under 40000', 'What is your return policy?'.\n"
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
        # Dispatch to the right handler
        if action == "show_cart":
            show_cart_handler = ShowCartHandler(get_user_id())
            show_cart_handler.handle()

        elif action == "add_to_cart":
            add_to_cart_handler = AddToCartHandler(get_user_id(), fetch_products)
            product_id = res.get("product_id") or res.get("id")
            add_to_cart_handler.handle(product_id)

        elif action == "remove_from_cart":
            remove_from_cart_handler = RemoveFromCartHandler(get_user_id())
            product_id = res.get("product_id") or res.get("id")
            remove_from_cart_handler.handle(product_id)

        elif action == "search_products":
            search_products_handler = SearchProductsHandler(fetch_products)
            filters = extract_filters(res)
            search_products_handler.handle(filters)

        elif action == "faq":
            faq_handler = FAQHandler()
            query = res.get("query")
            faq_handler.handle(query if query else "")

        elif action == "reply":
            print(f"Bot: {res.get('message','')}")

        else:
            print("Unknown action. LLM output:", res)

        messages.append({"role": "assistant", "content": llm_response})

if __name__ == "__main__":
    main()
