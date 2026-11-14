import re
from config import ASSISTANT_VOICES
from local_responses import normalize_input
from commands import SWITCH_TO_FEMALE_COMMAND, SWITCH_TO_MALE_COMMAND, TOGGLE_VOICE_GENDER_COMMAND, PRONUNCIATION_MAP

CURRENT_VOICE = ASSISTANT_VOICES["female"]


def preprocess_text(text):
    text = text.replace("\n", ". ")
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[*_~`#-]', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"^\s*[-•]\s*", "", text, flags=re.MULTILINE)

    for word, replacement in PRONUNCIATION_MAP.items():
        text = text.replace(word, replacement)

    return text


def get_current_voice():
    return CURRENT_VOICE


def voice_choices(user_input):
    global CURRENT_VOICE
    user_input = normalize_input(user_input)

    if user_input in SWITCH_TO_FEMALE_COMMAND:
        CURRENT_VOICE = ASSISTANT_VOICES["female"]
        return True

    if user_input in SWITCH_TO_MALE_COMMAND:
        CURRENT_VOICE = ASSISTANT_VOICES["male"]
        return True

    if user_input in TOGGLE_VOICE_GENDER_COMMAND:
        if CURRENT_VOICE == ASSISTANT_VOICES["female"]:
            CURRENT_VOICE = ASSISTANT_VOICES["male"]
        else:
            CURRENT_VOICE = ASSISTANT_VOICES["female"]
        return True

    return False
