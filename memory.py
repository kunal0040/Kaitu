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


MEMORY_CATEGORY = ["identity", "preferences", "education", "personal"]


def remember_fact(category, fact):
    memory = load_memory()

    if category not in MEMORY_CATEGORY:
        return False

    if category not in memory:
        memory[category] = []

    if fact in memory[category]:
        return False

    memory[category].append(fact)
    save_memory(memory)
    return True


def get_memory():
    return load_memory()


def get_memory_context():
    memory = load_memory()

    return f"""
    Known information about the user:
    {memory}
    """


def forget_fact(category, fact):
    memory = load_memory()

    if category not in memory:
        return False

    if fact not in memory[category]:
        return False

    memory[category].remove(fact)

    if not memory[category]:
        del memory[category]

    save_memory(memory)

    return True


conversation_history = []

MAX_HISTORY = 10


def add_message(role, content):
    conversation_history.append({"role": role, "content": content})
    trim_history()


def trim_history():
    global conversation_history
    conversation_history = conversation_history[-MAX_HISTORY:]


def get_conversation_history():
    return conversation_history.copy()


def clear_conversation_history():
    conversation_history.clear()
