import os
from groq import Groq
from memory import load_memory, get_conversation_history
from config import MODEL_NAME_GROQ, SYSTEM_PROMPT

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def ask(prompt):
    memory = load_memory()

    memory_context = f"""
    Known information about the user:
    {memory}
    """
    history = get_conversation_history()

    messages = [{"role": "system", "content": SYSTEM_PROMPT + memory_context}]

    for message in history:
        messages.append({"role": message["role"], "content": message["content"]})

    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=MODEL_NAME_GROQ,
        messages=messages,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=True,
    )

    response_text = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="", flush=True)

    return response_text
