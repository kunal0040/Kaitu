from router import route_input
from config import ASSISTANT_NAME, USER_NAME
from local_responses import normalize_input
from audio import handle_voice_mode


def main():
    print(f"{ASSISTANT_NAME} is Online...")

    while True:
        user_input = input("\nYou: ")

        if not user_input.strip():
            continue

        command = normalize_input(user_input)
        result = handle_voice_mode(command)

        if result == "exit":
            break

        if result == "keyboard":
            continue

        try:
            response = route_input(user_input)

            if response == "exit":
                print(f"{ASSISTANT_NAME}: Goodbye! Have a great day {USER_NAME}!")
                break

            print(f"{ASSISTANT_NAME}: {response}")

        except Exception as error:
            print(f"[Something Went Wrong]: {error}")


if __name__ == "__main__":
    main()
