from utils.helpers import print_products

class SearchProductsHandler:
    def __init__(self, fetch_products_fn):
        self.fetch_products = fetch_products_fn

    def handle(self, filters):
        products = self.fetch_products(filters, page=1, limit=12)
        print("Products matching filters:")
        print_products(products)
