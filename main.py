import pyttsx3
import speech_recognition as sr
from router import route_input
from config import ASSISTANT_NAME, USER_NAME

r = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()
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
            with sr.Microphone() as source:
                print("\nListening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                
            text = r.recognize_google(audio)
            print(f"You: {text}")
            user_input = text.strip()

        except sr.UnknownValueError:
            error_message = f"Sorry, I could not understand the audio. Please try again {USER_NAME}."
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