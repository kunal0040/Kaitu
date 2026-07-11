import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import MODEL_NAME, SYSTEM_PROMPT
from memory import load_memory, get_conversation_history

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def ask(prompt):

    memory = load_memory()

    memory_context = f"""
    Known information about the user:
    {memory}
    """

    history = get_conversation_history()
    contents = []

    for message in history:
        role = message["role"]

        if role == "assistant":
            role = "model"
        contents.append(
            types.Content(role=role, parts=[types.Part(text=message["content"])])
        )

    contents.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT + memory_context
        ),
    )

    return response.text
