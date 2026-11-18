from router import route_input
from config import ASSISTANT_NAME, USER_NAME
from audio import handle_voice_mode, voice_session
from local_response.input_analyzer import (
    input_processor,
    correct_command_input,
    is_farewell,
    is_greeting,
)


def main():
    print(f"{ASSISTANT_NAME} is Online...")
    is_greeting()

    while True:
        user_input = input(f"\n{USER_NAME}: ")

        if not user_input.strip():
            continue

        corrected_input = correct_command_input(user_input)
        processed_input = input_processor(corrected_input)
        mode_func = handle_voice_mode(processed_input)

        if mode_func:

            result = voice_session(initial_mode=mode_func)

            if result == "exit":
                break
            if result == "keyboard":
                print("\nKeyboard mode restored.")
                continue

        try:
            response = route_input(user_input, corrected_input, processed_input)

            print(f"{ASSISTANT_NAME}: {response}")

            if is_farewell(processed_input):
                break

        except Exception as error:
            print(f"[Something Went Wrong]: {error}")


if __name__ == "__main__":
    main()
