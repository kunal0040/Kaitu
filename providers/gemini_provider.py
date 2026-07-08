import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import MODEL_NAME, SYSTEM_PROMPT
from memory import load_memory

load_dotenv()

memory = load_memory()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

memory_context = f"""
Known information about the user:
{memory}
"""

chat = client.chats.create(
    model=MODEL_NAME,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT + memory_context
    ),
)


def ask(prompt):
    response = chat.send_message(prompt)
    return response.text
