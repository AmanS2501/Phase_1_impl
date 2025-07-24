# from core.intent_detection import IntentDetector
# from core.entity_extraction import EntityExtractor
# from core.state_manager import StateManager
# from core.dialog_manager import DialogManager
# from chains.chains import ChainDispatcher

# def main():
#     intent_detector = IntentDetector()
#     entity_extractor = EntityExtractor()
#     dialog_manager = DialogManager()
#     state_manager = StateManager()
#     chain_dispatcher = ChainDispatcher()
#     user_id = "user1"

#     while True:
#         user_input = input("You: ")
#         greeting = dialog_manager.get_greeting()
#         if greeting:
#             print(f"Bot: {greeting}")
#         intent = intent_detector.detect(user_input)
#         entities = entity_extractor.extract(user_input, intent)
#         product_id = "prod-12345"  # Example usage
#         category = "mobile-accessories"  # Example usage
#         response = chain_dispatcher.dispatch(intent, entities, user_input, user_id, product_id, category)
#         print(f"Bot: {response}")

# if __name__ == "__main__":
#     main()


# from core.intent_detection import IntentDetector
# from core.entity_extraction import EntityExtractor
# from core.state_manager import StateManager
# from core.dialog_manager import DialogManager
# from chains.chains import ChainDispatcher

# def main():
#     intent_detector = IntentDetector()
#     entity_extractor = EntityExtractor()
#     dialog_manager = DialogManager()
#     state_manager = StateManager()
#     chain_dispatcher = ChainDispatcher()
#     user_id = "user1"
#     # Available mock product/category
#     default_product_id = "p001"
#     default_category = "mobile-accessories"

#     while True:
#         user_input = input("You: ")
#         greeting = dialog_manager.get_greeting()
#         if greeting:
#             print(f"Bot: Welcome!!")
#         intent = intent_detector.detect(user_input)
#         entities = entity_extractor.extract(user_input, intent)
#         # Use mock product/category from mock data for demo
#         response = chain_dispatcher.dispatch(intent, entities, user_input, user_id, default_product_id, default_category)
#         print(f"Bot: {response}")

# if __name__ == "__main__":
#     main()


from core.intent_detection import IntentDetector
from core.entity_extraction import EntityExtractor
from core.state_manager import StateManager
from core.dialog_manager import DialogManager
from chains.chains import ChainDispatcher
from utils.helpers import append_chat_log, analyze_chat_log

def user_login():
    user_id = input("Please enter your user ID: ").strip()
    password = input("Please enter your password: ").strip()
    print(f"Welcome, {user_id}!")
    return user_id  # password is not checked in this mock

def print_cart_analysis(chain_disp):
    summary, details = chain_disp.get_cart_summary()
    print("Your previous cart analysis:")
    print(summary)
    if details:
        print("Cart items:")
        for d in details:
            print("-", d)

def print_chat_analysis(user_id):
    history = analyze_chat_log(user_id, 5)
    if history:
        print("Last few conversations:")
        for turn in history:
            print(f"You: {turn.get('user')}")
            print(f"Bot: {turn.get('bot')}")
    else:
        print("No previous chat history found.")

def main():
    user_id = user_login()
    intent_detector = IntentDetector()
    entity_extractor = EntityExtractor()
    dialog_manager = DialogManager()
    state_manager = StateManager()
    chain_dispatcher = ChainDispatcher(user_id)

    print_cart_analysis(chain_dispatcher)
    print_chat_analysis(user_id)
    print("\nLet's start chatting.")

    while True:
        user_input = input("You: ")
        greeting = dialog_manager.get_greeting()
        if greeting:
            print(f"Bot: {greeting}")
            append_chat_log(user_id, {"user": "", "bot": greeting})
        intent = intent_detector.detect(user_input)
        entities = entity_extractor.extract(user_input, intent)

        product_id = None
        category = None

        # For add/remove to/from cart, prompt for product realtime
        if intent == "CART_ASSIST":
            all_products = chain_dispatcher.mcp.products
            print("Available products:")
            for item in all_products:
                print(f"{item['product_id']}: {item['name']} (₹{item['price']})")
            product_id = input("Enter product_id to add/remove: ").strip()

        # For navigation, prompt for category
        if intent == "SMART_NAVIGATION":
            print("Available categories:")
            for cat_key in chain_dispatcher.mcp.categories:
                print(cat_key)
            category = input("Enter category for navigation: ").strip()

        bot_response = chain_dispatcher.dispatch(
            intent, entities, user_input, product_id, category
        )

        print(f"Bot: {bot_response}")
        append_chat_log(user_id, {"user": user_input, "bot": bot_response})

if __name__ == "__main__":
    main()
