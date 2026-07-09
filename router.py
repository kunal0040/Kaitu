from brain import ask_assistant
from local_responses import get_local_response, LOCAL_PHRASES, normalize_input
from command_engine import detect_command, execute_command
from memory_manager import handle_memory_command


def route_input(user_input):
    normalized_input = normalize_input(user_input)

    if normalized_input in LOCAL_PHRASES["farewell"]:
        return "exit"

    local_response = get_local_response(user_input)

    if local_response:
        return local_response
    
    memory_response = handle_memory_command(user_input)
    if memory_response:
        return memory_response
    
    command_data = detect_command(user_input)

    if command_data:
        command_response = execute_command(command_data)

        if command_response:
            return command_response

    return ask_assistant(user_input)