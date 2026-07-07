TARGET_ALIASES = {
    "gpt": "chatgpt",
    "chat gpt": "chatgpt",
    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "yt": "youtube",
    "insta": "instagram",
    "calc": "calculator",
}


COMMAND_ALIASES = {
    "open": "open",
    "launch": "open",
    "start": "open",
    "run": "open",
    "search": "search",
    "find": "search",
    "google": "search",
}


def normalize_target(target):

    target = target.lower().strip()
    return TARGET_ALIASES.get(target, target)

