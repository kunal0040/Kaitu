from provider_manager import ask_provider
from memory import add_message
from memory_manager import handle_pending_memory_action


def ask_assistant(prompt):

    pending_response = handle_pending_memory_action(prompt)

    if pending_response is not None:
        return pending_response

    normalized_prompt = prompt.lower().strip()

    if normalized_prompt.startswith("think "):
        mode = "thinking"
        actual_prompt = prompt[6:].strip()

    elif normalized_prompt.startswith("ola "):
        mode = "local"
        actual_prompt = prompt[4:].strip()

    else:
        mode = "cloud"
        actual_prompt = prompt

    response = ask_provider(actual_prompt, mode=mode)

    add_message("user", actual_prompt)
    add_message("assistant", response)

    return response
