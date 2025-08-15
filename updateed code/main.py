import json
from mcp.server.fastmcp import FastMCP

# from fastmcp import MCPClient
from core.groq_llm import GroqLLM
from prompt.system_prompt import SYSTEM_PROMPT
from utils.helpers import extract_filters

# MCP server configuration — update host/port if needed.
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 23232  # Or whatever your fastMCP server is running on

def get_user_id():
    user_id = input("Enter your user_id: ").strip()
    if not user_id:
        print("User ID cannot be empty. Please try again.")
        return get_user_id()
    return user_id

def main():
    client = FastMCP(MCP_SERVER_HOST, port=MCP_SERVER_PORT)  # Connect once
    llm = GroqLLM()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(
        "Welcome! Try: 'show my cart', 'add <product_id> to cart', "
        "'remove <product_id> from cart', 'show electronics under 40000', 'What is your return policy?'.\n"
        "Type 'exit' to quit."
    )
    user_id = get_user_id()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
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
            result = client.call_tool("show_cart", {"user_id": user_id})
            if not result:
                print("Your cart is empty.")
            else:
                print("Your cart:")
                for item in result:
                    print(f"{item.get('id','N/A')}: {item.get('title','Unknown')} (₹{item.get('price','N/A')})")

        elif action == "add_to_cart":
            product_id = res.get("product_id") or res.get("id")
            # Product API via MCP tool
            products = client.call_tool("search_products", {
                "filters": {"category": "all"}, "page": 1, "limit": 50
            })
            product = next((p for p in products if p.get("id") == product_id), None)
            if not product:
                print("Invalid product_id.")
            else:
                result = client.call_tool("add_to_cart", {
                    "user_id": user_id,
                    "product": product
                })
                print(result)

        elif action == "remove_from_cart":
            product_id = res.get("product_id") or res.get("id")
            result = client.call_tool("remove_from_cart", {
                "user_id": user_id,
                "product_id": product_id
            })
            print(result)

        elif action == "search_products":
            filters = extract_filters(res)
            products = client.call_tool("search_products", {
                "filters": filters,
                "page": 1,
                "limit": 12
            })
            print("Products matching filters:")
            for p in products:
                print(f"{p.get('id','N/A')}: {p.get('title','Unknown')} (₹{p.get('price','N/A')})")

        elif action == "faq":
            query = res.get("query", "")
            answer = client.call_tool("faq", {"query": query})
            print(answer)

        elif action == "reply":
            print(f"Bot: {res.get('message','')}")

        else:
            print("Unknown action. LLM output:", res)

        messages.append({"role": "assistant", "content": llm_response})

if __name__ == "__main__":
    main()
