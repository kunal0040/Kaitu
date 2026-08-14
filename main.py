from router import route_input
from config import ASSISTANT_NAME, USER_NAME
from local_responses import normalize_input, remove_wake_word
from audio import handle_voice_mode, voice_session


def main():
    print(f"{ASSISTANT_NAME} is Online...")

    while True:
        user_input = input("\nYou: ")

        if not user_input.strip():
            continue

        command = normalize_input(user_input)
        command = remove_wake_word(command)

        mode_func = handle_voice_mode(command)

        if mode_func:

            result = voice_session(initial_mode=mode_func)

            if result == "exit":
                break
            if result == "keyboard":
                print("\nKeyboard mode restored.")
                continue

        try:
            response = route_input(command)

            if response == "exit":
                print(f"{ASSISTANT_NAME}: Goodbye! Have a great day {USER_NAME}!")
                break

            print(f"{ASSISTANT_NAME}: {response}")

        except Exception as error:
            print(f"[Something Went Wrong]: {error}")


if __name__ == "__main__":
    main()
