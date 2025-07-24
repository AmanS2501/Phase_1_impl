# from handlers.faq_handler import FAQHandler
# from handlers.order_status_handler import OrderStatusHandler
# from handlers.product_discovery_handler import ProductDiscoveryHandler
# from handlers.cart_handler import CartHandler
# from handlers.navigation_handler import NavigationHandler
# from handlers.agent_handoff_handler import AgentHandoffHandler
# from mcp_client.mcp_api import MCPClient
# from core.groq_model import GroqChatModel

# class ChainDispatcher:
#     def __init__(self):
#         self.mcp = MCPClient()
#         self.faq = FAQHandler()
#         self.order = OrderStatusHandler(self.mcp)
#         self.product = ProductDiscoveryHandler(self.mcp)
#         self.cart = CartHandler(self.mcp)
#         self.nav = NavigationHandler(self.mcp)
#         self.agent = AgentHandoffHandler()
#         self.groq_model = GroqChatModel()  # Initialize Groq LLM

#     def generate_llm_response(self, user_input):
#         messages = [
#             {"role": "system", "content": "You are a helpful ecommerce assistant."},
#             {"role": "user", "content": user_input}
#         ]
#         return self.groq_model.generate_response(messages)

#     def dispatch(self, intent, entities, user_input, user_id=None, product_id=None, category=None):
#         if intent == "FAQ":
#             return self.faq.handle(user_input)
#         if intent == "ORDER_STATUS":
#             return self.order.handle(entities)
#         if intent == "PRODUCT_DISCOVERY":
#             return self.product.handle(entities)
#         if intent == "CART_ASSIST":
#             return self.cart.handle(entities, user_id, product_id)
#         if intent == "SMART_NAVIGATION":
#             return self.nav.handle(category)
#         if intent == "AGENT_HANDOFF":
#             return self.agent.handle(user_input)
#         # Fallback: use Groq LLM for assistant response
#         return self.generate_llm_response(user_input)


# from handlers.faq_handler import FAQHandler
# from handlers.order_status_handler import OrderStatusHandler
# from handlers.product_discovery_handler import ProductDiscoveryHandler
# from handlers.cart_handler import CartHandler
# from handlers.navigation_handler import NavigationHandler
# from handlers.agent_handoff_handler import AgentHandoffHandler
# from mcp_client.mcp_api import MCPClient
# from core.groq_model import GroqChatModel

# class ChainDispatcher:
#     def __init__(self):
#         self.mcp = MCPClient()
#         self.faq = FAQHandler()
#         self.order = OrderStatusHandler(self.mcp)
#         self.product = ProductDiscoveryHandler(self.mcp)
#         self.cart = CartHandler(self.mcp)
#         self.nav = NavigationHandler(self.mcp)
#         self.agent = AgentHandoffHandler()
#         self.groq_model = GroqChatModel()

#     def generate_llm_response(self, user_input):
#         messages = [
#             {"role": "system", "content": "You are a helpful ecommerce assistant."},
#             {"role": "user", "content": user_input}
#         ]
#         return self.groq_model.generate_response(messages)

#     def dispatch(self, intent, entities, user_input, user_id=None, product_id=None, category=None):
#         if intent == "FAQ":
#             return self.faq.handle(user_input)
#         if intent == "ORDER_STATUS":
#             return self.order.handle(entities)
#         if intent == "PRODUCT_DISCOVERY":
#             return self.product.handle(entities)
#         if intent == "CART_ASSIST":
#             return self.cart.handle(entities, user_id, product_id)
#         if intent == "SMART_NAVIGATION":
#             return self.nav.handle(category)
#         if intent == "AGENT_HANDOFF":
#             return self.agent.handle(user_input)
#         return self.generate_llm_response(user_input)


from handlers.faq_handler import FAQHandler
from handlers.order_status_handler import OrderStatusHandler
from handlers.product_discovery_handler import ProductDiscoveryHandler
from handlers.cart_handler import CartHandler
from handlers.navigation_handler import NavigationHandler
from handlers.agent_handoff_handler import AgentHandoffHandler
from core.groq_model import GroqChatModel
from mcp_client.mcp_api import MCPClient
from handlers.show_cart_handler import ShowCartHandler

class ChainDispatcher:
    def __init__(self, user_id):
        self.mcp = MCPClient(user_id)
        self.faq = FAQHandler()
        self.mcp = MCPClient(user_id)
        self.order = OrderStatusHandler(self.mcp)
        self.product = ProductDiscoveryHandler(self.mcp)
        self.cart = CartHandler(self.mcp)
        self.show_cart = ShowCartHandler(self.mcp)
        self.nav = NavigationHandler(self.mcp)
        self.agent = AgentHandoffHandler()
        self.groq_model = GroqChatModel()
        self.user_id = user_id

    def generate_llm_response(self, user_input):
        messages = [
            {"role": "system", "content": "You are a helpful ecommerce assistant."},
            {"role": "user", "content": user_input}
        ]
        return self.groq_model.generate_response(messages)

    def dispatch(self, intent, entities, user_input, product_id=None, category=None):
        if intent == "FAQ":
            return self.faq.handle(user_input)
        if intent == "ORDER_STATUS":
            return self.order.handle(entities)
        if intent == "PRODUCT_DISCOVERY":
            return self.product.handle(entities)
        if intent == "SHOW_CART":
            return self.show_cart.handle()
        elif intent == "CART_ASSIST":
            return self.cart.handle(entities, product_id)
        if intent == "SMART_NAVIGATION":
            return self.nav.handle(category)
        if intent == "AGENT_HANDOFF":
            return self.agent.handle(user_input)
        return self.generate_llm_response(user_input)

    def get_cart_summary(self):
        return self.mcp.analyze_cart()

    def get_cart_items(self):
        return self.mcp.get_cart()
