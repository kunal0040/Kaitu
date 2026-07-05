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

