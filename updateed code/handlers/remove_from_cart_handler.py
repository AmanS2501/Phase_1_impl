from fastmcp import MCPClient

class RemoveFromCartHandler:
    def __init__(self, mcp_client, user_id):
        self.mcp_client = mcp_client
        self.user_id = user_id

    def handle(self, product_id):
        result = self.mcp_client.call_tool("remove_from_cart", {
            "user_id": self.user_id,
            "product_id": product_id
        })
        print(result)
