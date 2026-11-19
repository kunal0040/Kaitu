from brain import ask_assistant
from data import save_conversation, handle_memory_command, add_message
from skills.calculator import looks_like_math_expression, execute_calculations
from local_response import (
    detect_command,
    execute_command,
    get_local_response,
    remove_wake_word,
)


def route_input(original_input, corrected_input, processed_input):

    response = get_local_response(processed_input)
    filtered_corrected_input = remove_wake_word(corrected_input)

    if response is None:
        response = handle_memory_command(filtered_corrected_input)

    if response is None and looks_like_math_expression(processed_input):
        response = execute_calculations(processed_input)

    if response is None:
        command_data = detect_command(processed_input)
        if command_data:
            response = execute_command(command_data)

    if response is None:
        response = ask_assistant(filtered_corrected_input)

    save_conversation(original_input, processed_input, response)
    add_message("user", original_input)
    add_message("assistant", response)

    return response
