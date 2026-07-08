import requests
from config import SYSTEM_PROMPT
from memory import load_memory

OLLAMA_URL = "http://localhost:11434/api/generate"
FAST_MODEL = "qwen2.5:3b"
THINKING_MODEL = "qwen3:4b"

memory = load_memory()

memory_context = f"""
Known information about the user:
{memory}
"""


def get_system_prompt(model_name):
    return SYSTEM_PROMPT + f"""

    Runtime information:
    You are currently running locally on the user's computer through Ollama.
    The underlying local model is {model_name}.
    You do not require cloud API credits for local inference.

    Do not identify the assistant as Qwen during normal conversation.

    If the user specifically asks about the underlying model, provider, or runtime,
    truthfully say that the current local model is {model_name} running through Ollama.
    """


def ask(prompt, thinking=False):

    if thinking:
        model_name = THINKING_MODEL
    else:
        model_name = FAST_MODEL

    payload = {
        "model": model_name,
        "system": get_system_prompt(model_name) + memory_context,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    return data["response"]

