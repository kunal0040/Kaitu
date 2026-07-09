from memory import remember_fact, get_memory
from config import USER_NAME

CATEGORY_KEYWORDS = {
    "preferences": [
        "prefer",
        "like",
        "love",
        "dislike",
        "hate",
        "favorite",
        "favourite",
    ],
    "education": [
        "study",
        "college",
        "university",
        "semester",
        "branch",
        "course",
        "student",
    ],
    "identity": [
        "my name",
        "i am",
        "i'm",
        "birthday",
        "born",
    ],
}

def detect_memory_category(fact):
    normalized_fact = fact.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized_fact:
                return category
            
    return "personal"

def remember(fact):
    fact = fact.strip()

    if not fact:
        return "What should I remember?"
    category = detect_memory_category(fact)

    remembered = remember_fact(category, fact)

    if not remembered:
        return f"I already know that, {USER_NAME}!"
    
    return f"I'll remember that {fact}, {USER_NAME}!"

def show_memory():
    memory = get_memory()

    if not memory:
        return f"I don't have any specific info about you {USER_NAME} yet."
    
    lines = []

    for category, facts in memory.items():
        if not facts:
            continue

        lines.append(f"{category.title()}:")

        for fact in facts:
            lines.append(f"- {fact}")

    if not lines:
        return f"I don't have any specific info about you {USER_NAME} yet."
    
    return "\n".join(lines)

MEMORY_COMMANDS = ["remember that ", "remember ", "keep in mind ", "do remember ", "memorize "]


def handle_memory_command(user_input):
    normalized_input = user_input.lower().strip()

    for command in MEMORY_COMMANDS:
        if normalized_input.startswith(command):
            fact = user_input[len(command):].strip()
            return remember(fact)
    
    if normalized_input in [
        "what do you remember about me",
        "what do you know about me",
        "what do you remember",
        "show memory",
        "show my memory",
    ]:
        return show_memory()
    
    return None
    


        