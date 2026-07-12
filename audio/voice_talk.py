from router import route_input
from audio import listen, speak, load_model
from local_responses import normalize_input
from config import ASSISTANT_NAME, USER_NAME

TALK_COMMAND = {
    "talk",
    "speak",
    "mic on",
    "let talk",
    "lets talk",
    "voice mode",
    "talk to me",
    "speak to me",
    "let me talk",
    "let speak",
    "lets speak",
    "listen to me",
    "enable voice",
    "turn on voice",
    "use microphone",
    "turn on the mic",
    "start listening",
    "switch to voice",
    "i want to speak",
    "take voice input",
    "let communicate",
    "lets communicate",
    "can i speak to you",
    "let me use my voice",
}

STOP_TALK_COMMAND = {
    "mic off",
    "mute mic",
    "text mode",
    "stop audio",
    "let me type",
    "stop talking",
    "turn off mic",
    "ill type now",
    "i will type now",
    "disable voice",
    "keyboard mode",
    "stop listening",
    "turn off voice",
    "switch to text",
    "i want to type",
    "switch to typing",
}

model = load_model()


def voice_mode():

    print("\nVoice mode activated.")

    while True:

        try:
            user_input = listen(model)
            print(f"You: {user_input}")

            if normalize_input(user_input) in STOP_TALK_COMMAND:
                speak(f"Had a nice convo with you {USER_NAME}!")
                print("Returning to keyboard mode.\n")
                return "keyboard"

            response = route_input(user_input)

            if response == "exit":
                speak("Goodbye!")
                return "exit"

            print(f"{ASSISTANT_NAME}: {response}")
            speak(response)

        except RuntimeError:
            error_message = f"\nI'm unable to recognise your command, {USER_NAME}."
            print(error_message)
            speak(error_message)
            continue
