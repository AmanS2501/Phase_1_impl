from fastmcp import MCPClient

class FAQHandler:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client

    def handle(self, query):
        answer = self.mcp_client.call_tool("faq", {"query": query})
        print(answer)
