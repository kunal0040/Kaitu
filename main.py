import pyttsx3
from audio.speech_input import load_model, listen
from router import route_input
from config import ASSISTANT_NAME, USER_NAME

model = load_model()
engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 165)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

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