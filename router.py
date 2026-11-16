from brain import ask_assistant
from commands import LOCAL_PHRASES
from data.memory import handle_memory_command
from data.logs.conversation_logs import save_conversation
from command_engine import detect_command, execute_command
from local_responses import get_local_response, remove_wake_word
from skills.calculator import looks_like_math_expression, execute_calculations


def route_input(original_input, processed_input):

    if processed_input in LOCAL_PHRASES["farewell"]:
        return "exit"

    response = get_local_response(processed_input)

    if response is None:
        response = handle_memory_command(processed_input)

    if response is None and looks_like_math_expression(processed_input):
        response = execute_calculations(processed_input)

    if response is None:
        command_data = detect_command(processed_input)
        if command_data:
            response = execute_command(command_data)

    if response is None:
        response = ask_assistant(remove_wake_word(original_input))

    save_conversation(original_input, processed_input, response)

    return response
