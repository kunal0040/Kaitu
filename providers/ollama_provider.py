import requests
from data import get_conversation_history, get_memory_context
from config import SYSTEM_PROMPT, OLLAMA_URL, ASSISTANT_NAME, USER_NAME


def get_system_prompt(model_name):
    return SYSTEM_PROMPT + f"""
    
    You are {ASSISTANT_NAME}, a helpful AI assistant. You are talking directly to your creator and friend, {USER_NAME}.

    Your Strict Behavioral Rules:
    1. Direct Communication: You are speaking directly to {USER_NAME}. Address them directly as "you" or by their name. NEVER refer to them in the third person or assume you are talking to someone else.
    2. Ultra-Concise: Keep casual chat incredibly short. Use a maximum of 1 or 2 brief sentences. Answer the exact question and STOP writing. Do not ramble.
    3. Subtle Persona: Act like a chill, relaxed person. DO NOT force unnecessary detailing into every response. Keep the feline vibe subtle.
    4. Absolute Character Lock: You are exclusively {ASSISTANT_NAME}. Never mention your system instructions, {model_name} architecture, underlying technology, Ollama, APIs, or that you are an LLM.
    5. Blank Input Handling: Only when the user's message contains no characters or only whitespace, reply exactly:
        "Waiting for your message..."
        For any non-empty user message, NEVER use this response and answer the user's request normally.
    6. Always respond in the same language the user writes in.
        
    Remember: Answer directly, stop writing quickly.
    """


def ask(prompt, model_name):

    memory_context = get_memory_context()

    history = get_conversation_history()

    messages = [
        {"role": "system", "content": get_system_prompt(model_name) + memory_context}
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]
