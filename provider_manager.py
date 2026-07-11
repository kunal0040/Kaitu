from providers import gemini_provider, ollama_provider


def ask_provider(prompt, mode="cloud"):

    if mode == "thinking":
        # print("[OLLAMA THINKING]")
        return ollama_provider.ask(
            prompt,
            model_name="dolphin3"
        )
    
    if mode == "local":
        # print("[OLLAMA LOCAL]")
        return ollama_provider.ask(
            prompt,
            model_name="qwen2.5:3b"
        )

    try:
        # print("[GEMINI RESPONSE]")
        return gemini_provider.ask(prompt)

    except Exception:
        return ollama_provider.ask(prompt, model_name="qwen2.5:3b")