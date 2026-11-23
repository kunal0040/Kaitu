import re
import string
import random
import difflib
from datetime import datetime
from . import aliases, commands
from local_response import LOCAL_PHRASES, LOCAL_RESPONSES, WAKE_WORDS


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
            return user_input[match.end() :].lstrip(" \t,.:!?-")

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


def extract_strings(obj):
    found = []

    if isinstance(obj, str):
        found.append(obj.lower().strip())

    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            found.extend(extract_strings(item))

    elif isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str):
                found.append(key.lower().strip())
            found.extend(extract_strings(value))

    return found


def command_vocabulary():
    vocab = set()

    excluded_commands = {
        "LOCAL_RESPONSES",
        "PRONUNCIATION_MAP",
        "MEMORY_STATEMENTS", 
        "MATH_ANSWER_PREFIXS",
    }

    for name in dir(commands):
        if name.startswith("_") or name in excluded_commands:
            continue

        value = getattr(commands, name)
        string = extract_strings(value)

        for text in string:
            if text:
                vocab.add(text)
            for word in text.split():
                if len(word) > 1:
                    vocab.add(word)

    for name in dir(aliases):
        if name.startswith("_"):
            continue

        value = getattr(aliases, name)
        strings = extract_strings(value)

        for text in strings:
            if text:
                vocab.add(text)
            for word in text.split():
                if len(word) > 1:
                    vocab.add(word)

    return vocab


COMMAND_VOCAB = command_vocabulary()


def correct_command_input(text: str, cutoff: float = 0.75) -> str:

    if not text:
        return text

    original_text = text
    text = text.lower().strip()

    corrected_words = []

    vocabulary = COMMAND_VOCAB

    word_vocabulary = {
        word
        for phrase in vocabulary
        for word in phrase.split()
        if word.isalpha() and len(word) > 1
    }

    words = text.split()

    for word in words:

        if word in word_vocabulary:
            corrected_words.append(word)
            continue

        if not word.isalpha():
            corrected_words.append(word)
            continue

        if len(word) <= 1:
            corrected_words.append(word)
            continue

        candidates = [
            candidate
            for candidate in word_vocabulary
            if abs(len(candidate) - len(word)) <= 1
        ]

        if len(word) <= 3:
            threshold = 0.75

        elif len(word) <= 5:
            threshold = 0.82

        elif len(word) <= 8:
            threshold = 0.80

        else:
            threshold = cutoff

        matches = difflib.get_close_matches(word, candidates, n=1, cutoff=threshold)

        corrected_words.append(matches[0] if matches else word)

    corrected_text = " ".join(corrected_words)

    return corrected_text


def is_farewell(user_input):
    return input_processor(user_input) in LOCAL_PHRASES["farewell"]


def is_greeting():
    from data import save_conversation
    response = random.choice(LOCAL_RESPONSES["greeting"])
    save_conversation("Start", "Start", response)
    print(response)


def get_current_time():
    current_time = datetime.now().strftime("%I:%M %p")
    return current_time


def get_current_date():
    current_date = datetime.now().strftime("%A, %d %B %Y")
    return current_date
