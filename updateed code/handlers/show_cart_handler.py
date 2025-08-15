from fastmcp import MCPClient

class ShowCartHandler:
    def __init__(self, mcp_client, user_id):
        self.mcp_client = mcp_client
        self.user_id = user_id

    def handle(self):
        cart = self.mcp_client.call_tool("show_cart", {"user_id": self.user_id})
        if not cart:
            print("Your cart is empty.")
        else:
            print("Your cart:")
            for item in cart:
                print(f"{item.get('id', 'N/A')}: {item.get('title', 'Unknown')} (₹{item.get('price','N/A')})")
