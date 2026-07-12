import os
import wave
import winsound
from piper import PiperVoice, SynthesisConfig
from config import PIPER_VOICES

TEMP_AUDIO = "_temp_speech.wav"
_voice = None
config = SynthesisConfig(length_scale=1.0)
ASSISTANT_VOICE = PIPER_VOICES["female"]
PRONUNCIATION_MAP = {
    "Kunal": "Koo-naaal",
}


def load_voice():
    global _voice

    if _voice is None:
        _voice = PiperVoice.load(ASSISTANT_VOICE)

    return _voice


def preprocess_text(text):

    for word, replacement in PRONUNCIATION_MAP.items():
        text = text.replace(word, replacement)

    return text


def speak(text):

    voice = load_voice()
    text = preprocess_text(text)

    with wave.open(TEMP_AUDIO, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file, syn_config=config)

    winsound.PlaySound(TEMP_AUDIO, winsound.SND_FILENAME)

    os.remove(TEMP_AUDIO)


if __name__ == "__main__":
    speak("Hello Kunal!!!, How are you")
