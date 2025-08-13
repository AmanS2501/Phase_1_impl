FAQ_DATA = {
    "return": "You can return any product within 7 days for a full refund.",
    "shipping": "We usually ship orders within 1-2 business days.",
    "payment": "We accept major cards, UPI, and net banking.",
    "warranty": "Most electronics come with a 1-year manufacturer's warranty.",
}

def faq(query):
    query = query.lower()
    for key in FAQ_DATA:
        if key in query:
            return FAQ_DATA[key]
    return "Sorry, no FAQ answer found. Please contact support."
