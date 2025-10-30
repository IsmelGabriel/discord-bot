# utils/memory.py
from collections import defaultdict

memory = defaultdict(list)

def add_message(user_id: int, role: str, content: str):
    """add a message to the user's memory."""
    memory[user_id].append({"role": role, "content": content})

def get_history(user_id: int):
    """return the message history for a user."""
    return memory[user_id]

def clear_history(user_id: int):
    """clear the message history for a user."""
    if user_id in memory:
        del memory[user_id]
