from providers import ask_gemini, ask_ollama
from config import FAST_MODEL, THINKING_MODEL, MEMORY_MODEL


def ask_provider(prompt, mode="cloud"):

    if mode == "thinking":
        # print("[OLLAMA THINKING]")
        try:
            return ask_ollama(prompt, model_name=THINKING_MODEL)

        except Exception:
            print("\nThinking model is unable to respond! Switching to another model...")
            return ask_ollama(prompt, model_name=MEMORY_MODEL)

    if mode == "local":
        # print("[OLLAMA LOCAL]")
        return ask_ollama(prompt, model_name=FAST_MODEL)

    try:
        # print("[GEMINI RESPONSE]")
        return ask_gemini(prompt)

    except Exception as e:
        print(f"[ERROR]: GEMINI FAILED. Switching to local model.\n{e}")
        return ask_ollama(prompt, model_name="qwen2.5:3b")
