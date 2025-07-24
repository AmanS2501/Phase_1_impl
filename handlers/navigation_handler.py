class NavigationHandler:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    def handle(self, category):
        link = self.mcp.get_category_link(category)
        return f"Here's the link to {category}: {link}" if link else "Category not found."
