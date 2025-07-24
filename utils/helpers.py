def sanitize_input(user_input):
    return user_input.strip().lower()
import json
import os

def append_chat_log(user_id, turn):
    log_file = f"chat_{user_id}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(turn, ensure_ascii=False) + "\n")

def load_chat_log(user_id, limit=5):
    log_file = f"chat_{user_id}.log"
    if not os.path.exists(log_file):
        return []
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()[-limit:]
        return [json.loads(line) for line in lines]

def analyze_chat_log(user_id, limit=5):
    log = load_chat_log(user_id, limit)
    return log
