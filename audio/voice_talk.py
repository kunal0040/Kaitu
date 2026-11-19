from router import route_input
from .speech_output import speak
from .voice_processing import voice_choices
from .speech_input import listen, load_model
from config import ASSISTANT_NAME, USER_NAME
from local_response import (
    input_processor,
    correct_command_input,
    is_farewell,
    RETURN_TO_TEXT_COMMAND,
    TWO_WAY_VOICE_COMMAND,
    TEXT_TO_SPEECH_COMMAND,
    VOICE_INPUT_COMMAND,
)

_model = None


def get_model():
    global _model

    if _model is None:
        _model = load_model()

    return _model


def two_way_voice_mode():

    print("\nVoice mode activated.\n")
    model = get_model()

    while True:

        try:
            user_input = listen(model)

            if not user_input.strip():
                continue

            print(f"{USER_NAME}: {user_input}")

            corrected_input = correct_command_input(user_input)
            processed_input = input_processor(corrected_input)

            if processed_input in RETURN_TO_TEXT_COMMAND:
                print("Returning to keyboard mode.")
                return "keyboard"

            next_mode = handle_voice_mode(processed_input)
            if next_mode:
                return next_mode

            new_voice = voice_choices(processed_input)
            if new_voice:
                speak("Voice updated.")
                continue

            response = route_input(user_input, corrected_input, processed_input)

            print(f"{ASSISTANT_NAME}: {response}")
            speak(response)

            if is_farewell(processed_input):
                return "exit"

        except RuntimeError:
            error_message = f"\nI'm unable to recognise your command, {USER_NAME}."
            print(error_message)
            speak(error_message)
            continue


def text_to_speech_mode():

    print("\nRead-Aloud mode activated.\nI will now speak my responses.\n")

    while True:

        try:

            user_input = input(f"{USER_NAME}: ")

            if not user_input.strip():
                continue

            corrected_input = correct_command_input(user_input)
            processed_input = input_processor(corrected_input)

            if processed_input in RETURN_TO_TEXT_COMMAND:
                print("\nReturning to keyboard mode.\n")
                return "keyboard"

            next_mode = handle_voice_mode(processed_input)
            if next_mode:
                return next_mode

            new_voice = voice_choices(processed_input)
            if new_voice:
                speak("Voice updated.")
                continue

            response = route_input(user_input, corrected_input, processed_input)

            print(f"{ASSISTANT_NAME}: {response}")
            speak(response)

            if is_farewell(processed_input):
                return "exit"

        except Exception as error:
            error_message = (
                f"\n[ERROR]: I encountered an error processing that, {USER_NAME}."
            )
            print(error_message)
            print(f"[Error Details]: {error}")
            speak("I encountered an error.")
            continue


def voice_input_mode():

    print("\nVoice input mode activated.\nSpeak naturally!\n")
    model = get_model()

    while True:

        try:
            user_input = listen(model)
            print(f"{USER_NAME}: {user_input}")

            if not user_input.strip():
                continue

            corrected_input = correct_command_input(user_input)
            processed_input = input_processor(corrected_input)

            if processed_input in RETURN_TO_TEXT_COMMAND:
                print("Returning to keyboard mode.\n")
                return "keyboard"

            next_mode = handle_voice_mode(processed_input)
            if next_mode:
                return next_mode

            new_voice = voice_choices(processed_input)
            if new_voice:
                speak("Voice updated.")
                continue

            response = route_input(user_input, corrected_input, processed_input)

            print(f"{ASSISTANT_NAME}: {response}")

            if is_farewell(processed_input):
                return "exit"

        except RuntimeError:
            error_message = f"\nI'm unable to recognise your command, {USER_NAME}."
            print(error_message)
            continue


VOICE_MODES = (
    (
        TWO_WAY_VOICE_COMMAND,
        two_way_voice_mode,
    ),
    (
        TEXT_TO_SPEECH_COMMAND,
        text_to_speech_mode,
    ),
    (
        VOICE_INPUT_COMMAND,
        voice_input_mode,
    ),
)


def handle_voice_mode(command):

    for commands, mode_func in VOICE_MODES:
        if command in commands:
            return mode_func

    return None


def voice_session(initial_mode=two_way_voice_mode):

    current_mode_func = initial_mode

    while True:
        result = current_mode_func()

        if result == "exit":
            return "exit"

        if result == "keyboard":
            return "keyboard"

        if callable(result):
            current_mode_func = result
            continue

        raise RuntimeError(f"Unknown voice session result: {result}")
