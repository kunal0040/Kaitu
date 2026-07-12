from memory import remember_fact, get_memory, load_memory, forget_fact, save_memory
from providers import analyze_memory
from config import USER_NAME

from memory import load_memory, save_memory, remember_fact

pending_memory_action = None

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

MEMORY_COMMANDS = [
    "remember that ",
    "keep in mind that ",
    "do remember that ",
    "memorize that ",
    "remember ",
    "keep in mind ",
    "do remember ",
    "memorize ",
]

FORGET_COMMANDS = [
    "remove my memory about that ",
    "delete from your mind that ",
    "remove my memory that ",
    "remove memory that ",
    "forget that ",
    "delete that ",
    "remove my memory about ",
    "delete from your mind ",
    "remove my memory ",
    "remove memory ",
    "forget ",
    "delete ",
]

VAGUE_MEMORY_PHRASES = [
    "i changed it",
    "things are different now",
    "that is no longer true",
    "my situation has changed",
    "it changed",
    "remember this",
    "remember that",
]

UPDATE_MARKERS = [
    "now",
    "currently",
    "changed",
    "switched",
    "moved",
    "became",
    "started",
    "stopped",
    "no longer",
    "instead",
    "updated",
    "increased",
    "decreased",
]


def has_explicit_update_marker(fact):
    normalized_fact = fact.lower()

    return any(marker in normalized_fact for marker in UPDATE_MARKERS)


def detect_memory_category(fact):
    normalized_fact = fact.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized_fact:
                return category

    return "personal"


def create_pending_memory_action(action, new_fact, matched_fact):
    global pending_memory_action

    if matched_fact is None:
        return f"I couldn't safely modify that memory, {USER_NAME}."

    pending_memory_action = {
        "action": action,
        "new_fact": new_fact,
        "matched_fact": matched_fact,
    }

    if action == "update":
        return (
            f"I currently remember '{matched_fact}'. "
            f"Should I replace it with '{new_fact}'?"
        )

    if action == "conflict":
        old_display = fact_to_user_perspective(matched_fact)
        new_display = fact_to_user_perspective(new_fact)

        return (
            f"I remember that {old_display}, but you're now telling me that "
            f"{new_display}. Should I replace the old memory?"
        )

    return f"I couldn't process that memory action, {USER_NAME}."


def handle_pending_memory_action(user_input):
    global pending_memory_action

    if pending_memory_action is None:
        return None

    normalized_input = user_input.lower().strip()

    YES_RESPONSES = {"yes", "yeah", "yep", "sure", "do it", "replace it", "update it"}

    NO_RESPONSES = {"no", "nope", "don't", "dont", "cancel", "keep it", "keep old"}

    if normalized_input in YES_RESPONSES:
        action = pending_memory_action["action"]
        new_fact = pending_memory_action["new_fact"]
        matched_fact = pending_memory_action["matched_fact"]

        pending_memory_action = None

        if action in {"update", "conflict"}:
            return handle_memory_update(new_fact, matched_fact)

    if normalized_input in NO_RESPONSES:
        pending_memory_action = None

        return f"Okay, I'll keep the old memory, {USER_NAME}."

    return "Please answer yes or no so I know whether to replace " "the old memory."


def remember(fact):
    fact = fact.strip()

    if not fact:
        return f"What should I remember {USER_NAME}?"

    if not validate_memory_fact(fact):
        return f"I need a more specific fact to remember, {USER_NAME}."

    memory = load_memory()

    existing_facts = []

    for facts in memory.values():
        existing_facts.extend(facts)

    result = analyze_memory(fact, existing_facts)

    relationship = result["relationship"]
    matched_fact = result["matched_fact"]

    actual_matched_fact = None

    if matched_fact is not None:
        normalized_match = matched_fact.lower().strip()

        for stored_fact in existing_facts:
            if stored_fact.lower().strip() == normalized_match:
                actual_matched_fact = stored_fact
                break

    if actual_matched_fact is not None:
        matched_fact = actual_matched_fact

    if relationship == "duplicate":
        return f"I already know that {USER_NAME}!"

    if relationship in {"update", "conflict"} and matched_fact is None:
        return (
            f"I recognized this as a memory {relationship}, "
            f"but couldn't safely identify the old memory, {USER_NAME}."
        )

    if relationship == "update":
        if has_explicit_update_marker(fact):
            return handle_memory_update(fact, matched_fact)

        return create_pending_memory_action(
            action="update", new_fact=fact, matched_fact=matched_fact
        )

    if relationship == "conflict":
        return create_pending_memory_action(
            action="conflict", new_fact=fact, matched_fact=matched_fact
        )

    if relationship == "uncertain":
        return (
            f"I'm not sure how this relates to what I already remember, "
            f"{USER_NAME}."
        )

    if relationship != "new":
        return f"I couldn't safely classify that memory, {USER_NAME}."

    category = detect_memory_category(fact)

    remembered = remember_fact(category, fact)

    if not remembered:
        return f"I couldn't save that memory, {USER_NAME}."

    display_fact = fact_to_user_perspective(fact)

    return f"I'll remember that {display_fact}, {USER_NAME}!"


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
            display_fact = fact_to_user_perspective(fact)
            lines.append(f"- {display_fact}")

    if not lines:
        return f"I don't have any specific info about you {USER_NAME} yet."

    return "\n".join(lines)


def handle_memory_command(user_input):
    normalized_input = user_input.lower().strip()

    for command in MEMORY_COMMANDS:
        if normalized_input.startswith(command):
            fact = user_input[len(command) :].strip()
            return remember(fact)

    for command in FORGET_COMMANDS:
        if normalized_input.startswith(command):
            target_fact = user_input[len(command) :].strip()
            return forget(target_fact)

    if normalized_input in [
        "what do you remember about me",
        "what do you know about me",
        "what do you remember",
        "show memory",
        "show my memory",
    ]:
        return show_memory()

    return None


def validate_memory_fact(fact):
    normalized_fact = fact.lower().strip()

    if not normalized_fact:
        return False

    if len(normalized_fact) < 4:
        return False

    if normalized_fact in VAGUE_MEMORY_PHRASES:
        return False

    return True


def forget(target_fact):
    memory = load_memory()

    all_facts = []

    for facts in memory.values():
        all_facts.extend(facts)

    result = analyze_memory(target_fact, all_facts)

    relationship = result["relationship"]
    matched_fact = result["matched_fact"]

    if relationship != "duplicate":
        return "I couldn't find that memory."

    if matched_fact is None:
        return "I couldn't find that memory."

    category, actual_stored_fact = find_actual_stored_fact(matched_fact)

    if category is None or actual_stored_fact is None:
        return "I found the memory but couldn't locate the stored fact."

    deleted = forget_fact(category, actual_stored_fact)

    if deleted:
        return f"I forgot that, {USER_NAME}."

    return f"I couldn't remove that memory, {USER_NAME}."


def handle_memory_update(new_fact, matched_fact):
    memory = load_memory()

    old_category = None
    actual_matched_fact = None

    normalized_matched_fact = matched_fact.lower().strip()

    for category, facts in memory.items():
        for stored_fact in facts:
            if stored_fact.lower().strip() == normalized_matched_fact:
                old_category = category
                actual_matched_fact = stored_fact
                break

        if old_category is not None:
            break

    if old_category is None:
        return f"I couldn't find the old memory to update, {USER_NAME}."

    memory[old_category].remove(actual_matched_fact)

    if not memory[old_category]:
        del memory[old_category]

    new_category = detect_memory_category(new_fact)

    if new_category not in memory:
        memory[new_category] = []

    memory[new_category].append(new_fact)

    save_memory(memory)

    return f"I've updated that, {USER_NAME}."


def fact_to_user_perspective(fact):
    fact = fact.strip()
    normalized = fact.lower()

    replacements = [
        ("i am ", "you are "),
        ("i'm ", "you're "),
        ("i was ", "you were "),
        ("i have ", "you have "),
        ("i've ", "you've "),
        ("i had ", "you had "),
        ("i do ", "you does "),
        ("mine ", "yours "),
        ("my ", "your "),
        ("i ", "you "),
    ]

    for old, new in replacements:
        if normalized.startswith(old):
            return new + fact[len(old) :]

    return fact


def find_actual_stored_fact(target_fact):
    memory = load_memory()

    normalized_target = target_fact.lower().strip()

    for category, facts in memory.items():
        for stored_fact in facts:
            if stored_fact.lower().strip() == normalized_target:
                return category, stored_fact

    return None, None
