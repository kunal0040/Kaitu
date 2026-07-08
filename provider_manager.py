from providers import gemini_provider, ollama_provider


def ask_provider(prompt, thinking=False):

    if thinking:
        return ollama_provider.ask(
            prompt,
            thinking=True
        )

    try:
        return gemini_provider.ask(prompt)

    except Exception:
        return ollama_provider.ask(prompt)