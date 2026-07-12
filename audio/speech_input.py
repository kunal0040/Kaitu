import os
import tempfile
import speech_recognition as sr
from faster_whisper import WhisperModel
from config import WHISPER_DEVICE, WHISPER_MODEL


def load_model():

    try:
        model = WhisperModel(
            WHISPER_MODEL, device=WHISPER_DEVICE, compute_type="float16"
        )

    except Exception as e:
        print(f"GPU unavailable: {e}")
        print("Loading Whisper on CPU...")
        model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")

    return model


def record_audio():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(audio.get_wav_data())

    return temp_file.name


def transcribe_audio(model, audio_path):

    try:
        segments, info = model.transcribe(audio_path, beam_size=2)
        text = " ".join(segment.text for segment in segments).strip()
        return text

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


def listen(model):

    audio_path = record_audio()
    text = transcribe_audio(model, audio_path)

    return text
