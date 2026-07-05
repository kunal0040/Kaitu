import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import ASSISTANT_NAME, MODEL_NAME, SYSTEM_PROMPT
from memory import load_memory

memory = load_memory()

load_dotenv()
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
    )
)

def ask_assistant(prompt):
    response = chat.send_message(prompt)
    return response.text


if __name__ == "__main__":
    print(f"{ASSISTANT_NAME} is Online...")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print(f"{ASSISTANT_NAME}: Goodbye! Have a great day!")
            break

        if not user_input:
            continue

        try:
            reply = ask_assistant(user_input)
            print(f"{ASSISTANT_NAME}: {reply}")
        except Exception as error:
            print(f"[Something Went Wrong]: {error}")
