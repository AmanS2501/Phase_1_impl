import sys
import json
from mcp_tools.cart_tool import show_cart, add_to_cart, remove_from_cart
from mcp_tools.product_tool import search_products
from mcp_tools.faq_tool import faq

def stdio_server():
    print("MCP server running. Send JSON requests line by line:")
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())
            cmd = req.get("command")
            user_id = req.get("user_id")
            # Routing
            if cmd == "show_cart":
                result = show_cart(user_id)
            elif cmd == "add_to_cart":
                product = req["product"]
                result = add_to_cart(user_id, product)
            elif cmd == "remove_from_cart":
                product_id = req["product_id"]
                result = remove_from_cart(user_id, product_id)
            elif cmd == "search_products":
                filters = req.get("filters", {})
                result = search_products(filters)
            elif cmd == "faq":
                result = faq(req.get("query", ""))
            else:
                result = {"error": "Unknown command"}
            print(json.dumps(result))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    stdio_server()
