import os
import tempfile
import speech_recognition as sr
from faster_whisper import WhisperModel
from config import WHISPER_DEVICE, WHISPER_MODEL

_recognizer = None
_microphone = None
_ambient_calibrated = False


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


def get_recognizer():
    global _recognizer

    if _recognizer is None:
        _recognizer = sr.Recognizer()
    return _recognizer


def get_microphone():
    global _microphone

    if _microphone is None:
        _microphone = sr.Microphone()
    return _microphone


def record_audio():
    global _ambient_calibrated

    r = get_recognizer()
    mic = get_microphone()

    with mic as source:
        print("\nListening...")

        if not _ambient_calibrated:
            r.adjust_for_ambient_noise(source, duration=0.5)
            _ambient_calibrated = True

        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            return None

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

    if audio_path is None:
        return ""

    text = transcribe_audio(model, audio_path)

    return text
