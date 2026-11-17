from provider_manager import ask_provider


def ask_assistant(prompt):

    normalized_prompt = prompt.lower().strip()

    mode = "default"
    actual_prompt = prompt

    if normalized_prompt.startswith("cloud "):
        mode = "cloud"
        actual_prompt = prompt[6:].strip()

    elif normalized_prompt.startswith("think "):
        mode = "thinking"
        actual_prompt = prompt[6:].strip()

    elif normalized_prompt.startswith("ola "):
        mode = "local"
        actual_prompt = prompt[4:].strip()

    response = ask_provider(actual_prompt, mode=mode)

    return response
