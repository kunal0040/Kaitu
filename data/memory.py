import os
import json
import uuid
import random
import requests
from datetime import datetime
from config import OLLAMA_URL, TALK_MODEL, USER_NAME

SUMMARIZER_MODEL = TALK_MODEL
MEMORY_FILE = os.path.join("data", "memory.json")

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

MEMORY_SUMMARY_COMMANDS = [
    "what do you know about me",
    "what do you remember about me",
    "tell me what you know about me",
    "tell me what you remember about me",
    "tell me about myself",
    "show me my memory",
    "what's in my memory",
    "what is in my memory",
    "who am i to you",
    "do you know who i am",
    "what info do you have about me",
    "summarize what you know about me",
    "show my profile",
    "memory summary",
]

MEMORY_STATEMENTS = {
        "remember": [
            f"I'll keep in mind that {USER_NAME}.",
            f"Got it, {USER_NAME}, I'll remember that for next time.",
            f"Noted! I'll make sure to factor in {USER_NAME}'s preference.",
            f"Thanks for the heads-up, {USER_NAME}, I've saved that detail.",
        ],
        "forget": [
            f"Understood, {USER_NAME}. I'll drop this and never bring it up again.",
            f"Consider it forgotten, {USER_NAME}—my lips are sealed.",
            f"Got it, {USER_NAME}. Deleting that from my memory right now.",
            f"Say no more, {USER_NAME}. We will never speak of this again.",
        ],
    }

remember_msg = random.choice(MEMORY_STATEMENTS["remember"])
forget_msg = random.choice(MEMORY_STATEMENTS["forget"])

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"memories": []}

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return {"memories": []}

    if not isinstance(memory_data, dict):
        return {"memories": []}

    memory_data.setdefault("memories", [])
    return memory_data


def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def remember_fact(fact):
    memory_data = load_memory()

    for item in memory_data["memories"]:
        if item["memory"].strip().casefold() == fact.strip().casefold():
            return False

    new_memory = {
        "memory_id": f"mem_{uuid.uuid4().hex[:8]}",
        "memory": fact,
        "created_at": datetime.now().astimezone().isoformat()
    }
    memory_data["memories"].append(new_memory)
    save_memory(memory_data)
    return True


def forget_fact(fact):
    memory_data = load_memory()

    original_count = len(memory_data["memories"])

    memory_data["memories"] = [
        item for item in memory_data["memories"]
        if item["memory"].strip().casefold() != fact.strip().casefold()
    ]
    if len(memory_data["memories"]) == original_count:
        return False
    save_memory(memory_data)
    return True


def get_memory():
    return load_memory()


def memory_summary():
    memory_data = get_memory()
    memories = memory_data["memories"]

    if not memories:
        return "I don't have any specific facts abot you!!"

    memory_context = "\n".join(
        f"- {item['memory']}"
        for item in memories
    )

    prompt = f"""
    Here are the facts stored in your memory about {USER_NAME}:

    {memory_context}

    Tell {USER_NAME} what you know about them in a natural, conversational way.

    Instructions:
    - Address {USER_NAME} directly using "you" and "your" (e.g., "You are...", "You live in...").
    - Never speak as if you are the user. You are Kaitu, the assistant.
    - Use only the facts provided above. Do not invent or assume anything.
    - Organize related information naturally without unnecessary repetition.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": SUMMARIZER_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are Kaitu's memory engine. Summarize what you know about {USER_NAME} using second-person pronouns ('you', 'your')."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=120
        )
        
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return "Unable to connect to Ollama. Please check whether Ollama is running."

    except requests.exceptions.Timeout:
        return "Memory summarization timed out."

    except (requests.exceptions.RequestException, KeyError, ValueError):
        return "Unable to generate memory summary."


def handle_memory_command(user_input):
    text = user_input.lower().strip()

    for command in MEMORY_COMMANDS:
        if text.startswith(command.casefold()):
            fact = text[len(command):].strip()

            if not fact:
                return f"What should I remember about you, {USER_NAME}?"

            if remember_fact(fact):
                return remember_msg
            return f"I already know that {USER_NAME}!"

    for command in FORGET_COMMANDS:
        if text.startswith(command.casefold()):
            fact = text[len(command):].strip()

            if not fact:
                return f"What would you like me to forget about you {USER_NAME}?"

            if forget_fact(fact):
                return forget_msg
            return f"I think you haven't told me anything like that {USER_NAME}!"

    if text in MEMORY_SUMMARY_COMMANDS:
        return memory_summary()


def add_fact_to_memory(fact):
    remember_fact(fact)


def remove_fact_from_memory(fact):
    forget_fact(fact)


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
