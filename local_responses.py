import re
import random
import string
from datetime import datetime
from commands import LOCAL_PHRASES, LOCAL_RESPONSES, WAKE_WORDS


def normalize_input(user_input):

    normalized_input = user_input.lower().strip()

    keep_chars = "+-*/%()[]{}=<>"
    chars_to_remove = "".join(c for c in string.punctuation if c not in keep_chars)

    normalized_input = normalized_input.translate(
        str.maketrans("", "", chars_to_remove)
    )

    normalized_input = " ".join(normalized_input.split())

    return normalized_input


def remove_wake_word(user_input):

    if not user_input:
        return user_input

    for wake_word in sorted(WAKE_WORDS, key=len, reverse=True):

        pattern = rf"^\s*{re.escape(wake_word)}(?=$|[\s,.:!?-])"

        match = re.match(pattern, user_input, re.IGNORECASE)

        if match:
            return user_input[match.end():].lstrip(" \t,.:!?-")

    return user_input


def input_processor(user_input):
    
    removed_wakeword_input = remove_wake_word(user_input)
    processed_input = normalize_input(removed_wakeword_input)
    return processed_input


def get_local_response(user_input):

    normalized_input = normalize_input(user_input)

    for intent, phrases in LOCAL_PHRASES.items():
        if normalized_input in phrases:

            if intent == "time":
                return f"It's {get_current_time()}"

            elif intent == "date":
                return f"Today is {get_current_date()}"

            elif intent == "date and time":
                return f"It's {get_current_time()} of {get_current_date()}"

            return random.choice(LOCAL_RESPONSES[intent])

    return None


def is_farewell(user_input):
    return input_processor(user_input) in LOCAL_PHRASES["farewell"]


def is_greeting():
    print(random.choice(LOCAL_RESPONSES["greeting"]))

def get_current_time():
    current_time = datetime.now().strftime("%I:%M %p")
    return current_time


def get_current_date():
    current_date = datetime.now().strftime("%A, %d %B %Y")
    return current_date
