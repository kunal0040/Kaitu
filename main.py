from router import route_input
from local_responses import input_processor
from config import ASSISTANT_NAME, USER_NAME
from audio import handle_voice_mode, voice_session


def main():
    print(f"{ASSISTANT_NAME} is Online...")

    while True:
        user_input = input(f"\n{USER_NAME}: ")

        if not user_input.strip():
            continue

        processed_input = input_processor(user_input)

        mode_func = handle_voice_mode(processed_input)

        if mode_func:

            result = voice_session(initial_mode=mode_func)

            if result == "exit":
                break
            if result == "keyboard":
                print("\nKeyboard mode restored.")
                continue

        try:
            response = route_input(user_input, processed_input)

            if response == "exit":
                print(f"{ASSISTANT_NAME}: Goodbye! Have a great day {USER_NAME}!")
                break

            print(f"{ASSISTANT_NAME}: {response}")

        except Exception as error:
            print(f"[Something Went Wrong]: {error}")


if __name__ == "__main__":
    main()
