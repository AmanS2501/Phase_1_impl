class OrderStatusHandler:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    def handle(self, entities):
        order_id = entities.get("order_id")
        if not order_id:
            return "Please provide your order number."
        order = self.mcp.get_order_status(order_id)
        return f"Your order status is: {order['status']}" if 'status' in order else "Order not found."
