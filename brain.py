from provider_manager import ask_provider


def ask_assistant(prompt):
    normalized_prompt = prompt.lower().strip()

    if normalized_prompt.startswith("think "):
        actual_prompt = prompt[6:].strip()

        return ask_provider(actual_prompt, thinking=True)
    return ask_provider(prompt)
