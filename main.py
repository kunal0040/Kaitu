from router import route_input
from config import ASSISTANT_NAME, USER_NAME
from local_responses import normalize_input
from audio import voice_mode, TALK_COMMAND


def main():
    print(f"{ASSISTANT_NAME} is Online...\n")

    while True:
        user_input = input("You: ")

        if not user_input:
            continue

        if normalize_input(user_input) in TALK_COMMAND:
            result = voice_mode()

            if result == "exit":
                break
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
