from providers import gemini_provider, ollama_provider


def ask_provider(prompt, mode="cloud"):

    if mode == "thinking":
        return ollama_provider.ask(
            prompt,
            thinking=True,
            model_name="qwen3:4b"
        )
    
    if mode == "local":
        return ollama_provider.ask(
            prompt,
            thinking=False,
            model_name="qwen2.5:3b"
        )


    try:
        return gemini_provider.ask(prompt)

    except Exception as e:
        print(f"[Gemini failed, falling back to Ollama: {e}]")
        return ollama_provider.ask(prompt, model_name="qwen2.5:3b")