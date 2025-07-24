import re

class EntityExtractor:
    def extract(self, user_input: str, intent: str) -> dict:
        entities = {}
        if intent == "ORDER_STATUS":
            match = re.search(r'\b\d{5,}\b', user_input)
            if match:
                entities['order_id'] = match.group(0)
        if intent == "PRODUCT_DISCOVERY":
            price_match = re.search(r'under\s*₹?(\d+)', user_input)
            if price_match:
                entities['max_price'] = int(price_match.group(1))
            if "women" in user_input.lower() or "woman" in user_input.lower() or "female" in user_input.lower():
                entities["gender"] = "women"
            elif "men" in user_input.lower() or "man" in user_input.lower() or "male" in user_input.lower():
                entities["gender"] = "men"

        if intent == "CART_ASSIST":
            if "add" in user_input:
                entities["action"] = "add"
            elif "remove" in user_input:
                entities["action"] = "remove"

        if intent == "SHOW_CART":
            entities["show_cart"] = True


        return entities
