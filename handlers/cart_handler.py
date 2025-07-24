class CartHandler:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    def handle(self, entities, product_id):
        action = entities.get("action")
        if not action or not product_id:
            return "Please specify add/remove and a product ID."
        result = self.mcp.modify_cart(product_id, action)
        return result.get("message", "Cart updated.")
