from router import route_input
from config import ASSISTANT_NAME, USER_NAME
from audio.speech_input import load_model, listen
from audio.speech_output import speak

model = load_model()


def main():
    print(f"{ASSISTANT_NAME} is Online...")

    while True:
        try:
            text = listen(model)
            print(f"You: {text}")
            user_input = text.strip()

        except Exception:
            error_message = f"I'm unable to recognise your command, {USER_NAME}."
            print(error_message)
            speak(error_message)
            continue
            
        if not user_input:
            continue

        try:
            response = route_input(user_input)

            if response == "exit":
                print(f"{ASSISTANT_NAME}: Goodbye! Have a great day {USER_NAME}!")
                speak("Goodbye! Have a great day!")
                break

            print(f"{ASSISTANT_NAME}: {response}")
            speak(response)

        except Exception as error:
            print(f"[Something Went Wrong]: {error}")


if __name__ == "__main__":
    main()