from utils.helpers import print_products

class SearchProductsHandler:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

    def handle(self, filters):
        products = self.mcp_client.call_tool("search_products", {
            "filters": filters,
            "page": 1,
            "limit": 12
        })
        print("Products matching filters:")
        print_products(products)
