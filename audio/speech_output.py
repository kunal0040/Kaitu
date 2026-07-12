import os
import wave
import winsound
from piper import PiperVoice
from config import PIPER_MODEL
import os

TEMP_AUDIO = "temp_speech.wav"
_voice = None


def load_voice():
    global _voice
    
    if _voice is None:
        print("Loading Assistant Voice...")
        _voice = PiperVoice.load(PIPER_MODEL)
    
    return _voice


def speak(text):

    voice = load_voice()

    with wave.open(TEMP_AUDIO, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    winsound.PlaySound(TEMP_AUDIO, winsound.SND_FILENAME)

    os.remove(TEMP_AUDIO)


if __name__ == "__main__":
    speak("Hiiii")
    # speak("Hii Kunal! It's Kaitu.\nNow I can speak!!!\nLet's talk...")

