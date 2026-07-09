from providers import gemini_provider, ollama_provider


def ask_provider(prompt, mode="cloud"):

    if mode == "thinking":
        # print("[OLLAMA THINKING]")
        return ollama_provider.ask(
            prompt,
            model_name="qwen3:4b"
        )
    
    if mode == "local":
        # print("[OLLAMA LOCAL]")
        return ollama_provider.ask(
            prompt,
            model_name="qwen2.5:3b"
        )
    
    if mode == "dolphin":
        # print("[OLLAMA DOLPHIN]")
        return ollama_provider.ask(
            prompt,
            model_name="dolphin3"
        )


    try:
        # print("[GEMINI RESPONSE]")
        return gemini_provider.ask(prompt)

    except Exception as e:
        print(f"[Gemini failed, falling back to Ollama: {e}]")
        return ollama_provider.ask(prompt, model_name="qwen2.5:3b")