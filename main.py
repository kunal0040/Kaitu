from config import ASSISTANT_NAME
from router import route_input


def main():
    print(f"{ASSISTANT_NAME} is Online...")

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        try:
            response = route_input(user_input)

            if response == "exit":
                print(f"{ASSISTANT_NAME}: Goodbye! Have a great day!")
                break

            print(f"{ASSISTANT_NAME}: {response}")

        except Exception as error:
            print(f"[Something Went Wrong]: {error}")


if __name__ == "__main__":
    main()