from brain import ask_assistant
from local_responses import get_local_response


def route_input(user_input):
    normalized_input = user_input.lower().strip()

    if normalized_input in ["exit", "quit", "goodbye", "bye"]:
        return "exit"

    local_response = get_local_response(user_input)

    if local_response:
        return local_response

    return ask_assistant(user_input)