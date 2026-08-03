import os
import wave
import winsound
from .voice_processing import preprocess_text, get_current_voice
from piper import PiperVoice, SynthesisConfig

TEMP_AUDIO = "_temp_speech.wav"
_voice = None
_loaded_voice_path = None
config = SynthesisConfig(length_scale=1.0)


def load_voice():
    global _voice, _loaded_voice_path
    current_path = get_current_voice()

    if _voice is None or _loaded_voice_path != current_path:
        _voice = PiperVoice.load(current_path)
        _loaded_voice_path = current_path

    return _voice

def speak(text):

    voice = load_voice()
    text = preprocess_text(text)

    with wave.open(TEMP_AUDIO, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file, syn_config=config)

    winsound.PlaySound(TEMP_AUDIO, winsound.SND_FILENAME)

    os.remove(TEMP_AUDIO)

