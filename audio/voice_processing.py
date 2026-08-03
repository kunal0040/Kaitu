import re
from config import ASSISTANT_VOICES
from local_responses import normalize_input

CURRENT_VOICE = ASSISTANT_VOICES["female"]

SWITCH_TO_FEMALE_COMMAND = {
    "switch to female voice",
    "switch to female",
    "use a female voice",
    "change to female voice",
    "switch to a woman's voice",
    "sound like a female",
    "talk like a woman",
    "female voice please",
    "enable female voice",
    "change voice to female",
    "switch voice to female",
    "i want a female voice",
    "use a woman's voice",
    "make your voice female",
}

SWITCH_TO_MALE_COMMAND = {
    "switch to male voice",
    "switch to male",
    "use a male voice",
    "change to male voice",
    "switch to a man's voice",
    "sound like a male",
    "talk like a man",
    "talk like a guy",
    "male voice please",
    "enable male voice",
    "change voice to male",
    "switch voice to male",
    "i want a male voice",
    "use a man's voice",
    "make your voice male",
}

TOGGLE_VOICE_GENDER_COMMAND = {
    "change voice gender",
    "change gender",
    "change voice",
    "change your gender",
    "switch voice gender",
    "use a different voice",
    "swap voice",
    "toggle voice",
    "switch to the other voice",
    "use the opposite voice",
    "change your voice",
    "give me a different voice",
}

PRONUNCIATION_MAP = {
    "Kunal": "Koo-naaal",
}


def preprocess_text(text):
    text = text.replace("\n", ". ")
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'[*_~`#]', '', text)
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
