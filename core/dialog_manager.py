class DialogManager:
    def __init__(self):
        self.greeted = False
    def get_greeting(self):
        if not self.greeted:
            self.greeted = True
            return "Welcome! How can I assist you today?"
        return None
    def get_idle_timeout(self):
        return "Are you still there? Let me know if you need more help."
