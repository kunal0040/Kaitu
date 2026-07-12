from providers import (
    gemini_provider,
    ollama_provider,
    FAST_MODEL,
    THINKING_MODEL,
    MEMORY_MODEL,
)


def ask_provider(prompt, mode="cloud"):

    if mode == "thinking":
        # print("[OLLAMA THINKING]")
        try:
            return ollama_provider.ask(prompt, model_name=THINKING_MODEL)

        except Exception:
            print("\nThinking model is unable to respond! Switching to another model...")
            return ollama_provider.ask(prompt, model_name=MEMORY_MODEL)

    if mode == "local":
        # print("[OLLAMA LOCAL]")
        return ollama_provider.ask(prompt, model_name=FAST_MODEL)

    try:
        # print("[GEMINI RESPONSE]")
        return gemini_provider.ask(prompt)

    except Exception as e:
        print(f"[ERROR]: {e}")
        return ollama_provider.ask(prompt, model_name="qwen2.5:3b")
