class IntentDetector:
    def detect(self, user_input: str) -> str:
        keywords = {
            "order": "ORDER_STATUS",
            "status": "ORDER_STATUS",
            "refund": "FAQ",
            "return": "FAQ",
            "shoes": "PRODUCT_DISCOVERY",
            "add cart": "CART_ASSIST",
            "remove cart": "CART_ASSIST",
            "support": "AGENT_HANDOFF",
            "category": "SMART_NAVIGATION",
            "show my cart": "SHOW_CART",
            "show cart": "SHOW_CART",
            "my cart": "SHOW_CART",
        }
        for key, value in keywords.items():
            if key in user_input.lower():
                return value
        return "FAQ"
