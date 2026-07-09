import os
import json

MEMORY_FILE = "data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
        
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
        
    except json.JSONDecodeError:
        return {}
    
def save_memory(memory):
    os.makedirs("data", exist_ok=True)

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

conversation_history = []

MAX_HISTORY = 10

def add_message(role, content):
    conversation_history.append(
        {
            "role": role,
            "content": content
        }
    )
    trim_history()

def trim_history():
    global conversation_history
    conversation_history = conversation_history[-MAX_HISTORY:]

def get_conversation_history():
    return conversation_history.copy()

def clear_conversation_history():
    conversation_history.clear()