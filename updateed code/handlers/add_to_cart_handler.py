from fastmcp import MCPClient

class AddToCartHandler:
    def __init__(self, mcp_client, user_id):
        self.mcp_client = mcp_client
        self.user_id = user_id

    def handle(self, product):
        # 'product' should be a dict with at least 'id', 'title', 'price'
        result = self.mcp_client.call_tool("add_to_cart", {
            "user_id": self.user_id,
            "product": product
        })
        print(result)
