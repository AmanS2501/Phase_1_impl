class ShowCartHandler:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    def handle(self):
        cart = self.mcp.get_cart()
        if not cart:
            return "Your cart is empty."
        response = "Your cart contains:\n"
        for item in cart:
            response += f"- {item['name']} (₹{item['price']})\n"
        return response.strip()
