from brain import ask_assistant
from local_responses import get_local_response
from command_engine import detect_command, execute_command


def route_input(user_input):
    normalized_input = user_input.lower().strip()

    if normalized_input in ["exit", "quit", "goodbye", "bye"]:
        return "exit"

    local_response = get_local_response(user_input)

    if local_response:
        return local_response
    
    command_data = detect_command(user_input)

    if command_data:
        command_response = execute_command(command_data)

        if command_response:
            return command_response

    return ask_assistant(user_input)