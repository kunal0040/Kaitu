import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import MODEL_NAME, SYSTEM_PROMPT
from memory import load_memory


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

memory = load_memory()

memory_context = f"""
Known information about the user:
{memory}
"""


client = genai.Client(api_key=api_key)


chat = client.chats.create(
    model=MODEL_NAME,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT + memory_context
    )
)


def ask_assistant(prompt):
    response = chat.send_message(prompt)

    return response.text