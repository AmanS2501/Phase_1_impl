# class ProductDiscoveryHandler:
#     def __init__(self, mcp_client):
#         self.mcp = mcp_client
#     def handle(self, entities):
#         filters = {}
#         if "max_price" in entities:
#             filters["max_price"] = entities["max_price"]
#         if "gender" in entities:
#             filters["gender"] = entities["gender"]
#         products = self.mcp.search_products(filters)
#         if products:
#             return f"Found {len(products)} items. Top result: {products[0]['name']} - ₹{products[0]['price']}"
#         return "No products found matching your criteria."


class ProductDiscoveryHandler:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    def handle(self, entities):
        filters = {}
        if "max_price" in entities:
            filters["max_price"] = entities["max_price"]
        if "gender" in entities:
            filters["gender"] = entities["gender"]
        products = self.mcp.search_products(filters)
        if products:
            # List top 3 results
            result = f"Found {len(products)} items. Top results:\n"
            for p in products[:3]:
                result += f"- {p['name']} (₹{p['price']})\n"
            return result.strip()
        return "No products found matching your criteria."
