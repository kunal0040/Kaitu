import os
import json
import uuid
import random
import requests
from datetime import datetime
from local_response.input_analyzer import normalize_input
from config import OLLAMA_URL, TALK_MODEL, USER_NAME, ASSISTANT_NAME
from local_response.commands import (
    MEMORY_COMMANDS,
    FORGET_COMMANDS,
    MEMORY_STATEMENTS,
    MEMORY_SUMMARY_COMMANDS,
)

SUMMARIZER_MODEL = TALK_MODEL
MEMORY_FILE = os.path.join("data", "memory.json")

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

    normalized_fact = normalize_input(fact)

    for item in memory_data["memories"]:
        if normalize_input(item["memory"]) == normalized_fact:
            return False

    new_memory = {
        "memory_id": f"mem_{uuid.uuid4().hex[:8]}",
        "memory": fact,
        "created_at": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
    }
    memory_data["memories"].append(new_memory)
    save_memory(memory_data)
    return True


def forget_fact(fact):
    memory_data = load_memory()

    normalized_fact = normalize_input(fact)

    original_count = len(memory_data["memories"])

    memory_data["memories"] = [
        item
        for item in memory_data["memories"]
        if normalize_input(item["memory"]) != normalized_fact
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
        return f"I think you haven't told me anything about you yet!!"

    memory_context = "\n".join(f"- {item['memory']}" for item in memories)

    prompt = f"""
    Here are the facts stored in your memory about {USER_NAME}:

    {memory_context}

    Give {USER_NAME} a brief, direct summary of these facts.

    Instructions:
    - Address {USER_NAME} directly using "you" and "your" (e.g., "You are...", "You live in...").
    - Never speak as if you are the user. You are {ASSISTANT_NAME}, the assistant.
    - Use only the facts provided above. Do not invent or assume anything.
    - Return only the summary, without an introduction or extra commentary.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": SUMMARIZER_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are {ASSISTANT_NAME}'s memory engine. Summarize what you know about {USER_NAME} using second-person pronouns ('you', 'your').",
                    },
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        result = response.json()
        return result["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return (
            "Unable to connect to Ollama. Please check whether local model is running."
        )

    except requests.exceptions.Timeout:
        return "Memory summarization timed out."

    except (requests.exceptions.RequestException, KeyError, ValueError):
        return "Unable to generate memory summary."


def handle_memory_command(user_input):
    text = user_input.strip()
    normalized_text = normalize_input(user_input)

    for command in MEMORY_COMMANDS:
        if normalized_text.startswith(command.casefold()):
            fact = text[len(command) :].strip()

            if not fact:
                return f"What should I remember about you, {USER_NAME}?"

            if remember_fact(fact):
                return remember_msg
            return f"I already know that {USER_NAME}!"

    for command in FORGET_COMMANDS:
        if normalized_text.startswith(command.casefold()):
            fact = text[len(command) :].strip()

            if not fact:
                return f"What would you like me to forget about you {USER_NAME}?"

            if forget_fact(fact):
                return forget_msg
            return f"I think you haven't told me anything like that."

    if normalized_text in MEMORY_SUMMARY_COMMANDS:
        return memory_summary()


def get_memory_context():

    memories = get_memory()["memories"]

    if not memories:
        return ""

    memory_text = "\n".join(f"- {item['memory']}" for item in memories)

    return f"""
    LONG-TERM MEMORY ABOUT THE USER:

    {memory_text}

    Use these memories when relevant.
    Do not invent additional personal information.
    """


def add_fact_to_memory(fact):
    remember_fact(fact)


def remove_fact_from_memory(fact):
    forget_fact(fact)


conversation_history = []

MAX_HISTORY = 20


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
