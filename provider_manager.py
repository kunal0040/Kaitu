from providers import ask_gemini, ask_ollama
from config import FAST_MODEL, TALK_MODEL, MEMORY_MODEL


def ask_provider(prompt, mode="cloud"):

    if mode == "thinking":

        try:
            print("[GEMINI RESPONSE]")
            return ask_gemini(prompt)

        except Exception:
            print("[OLLAMA RESPONSE]")
            print("\n[ERROR]: Thinking model is unable to respond! Switching to local model...")
            return ask_ollama(prompt, model_name=MEMORY_MODEL)

    if mode == "local":
        print("[OLLAMA RESPONSE]")
        return ask_ollama(prompt, model_name=TALK_MODEL)

    print("[OLLAMA RESPONSE]")
    return ask_ollama(prompt, model_name=FAST_MODEL)
        
