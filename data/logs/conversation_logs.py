import json
from pathlib import Path
from datetime import datetime

conversation_log = []

LOG_FILE = Path(__file__).with_name("conversation_log.json")


def load_conversation_log():
    if LOG_FILE.exists():
        try:
            with LOG_FILE.open("r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

    return []


conversation_log = load_conversation_log()


def save_conversation(original_input, processed_input, response):

    conversation_log.append({
        "original_input": original_input,
        "processed_input": processed_input,
        "assistant_response": response,
        "conversation_time": datetime.now().strftime("%d-%m-%y %H:%M:%S")
    })

    with LOG_FILE.open("w", encoding="utf-8") as file:
        json.dump(conversation_log, file, ensure_ascii=False, indent=2)


def get_conversation_log():
    return conversation_log.copy()