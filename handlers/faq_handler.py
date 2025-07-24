class FAQHandler:
    STATIC_ANSWERS = {
        "refund": "Refunds are processed within 3-5 business days.",
        "return": "Returns are accepted within 15 days of delivery.",
        "shipping": "We ship all orders within 24 hours."
    }
    def handle(self, user_input):
        for key, ans in self.STATIC_ANSWERS.items():
            if key in user_input.lower():
                return ans
        return "Please specify your query."
