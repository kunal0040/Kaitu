import re

TARGET_ALIASES = {
    # AI
    "gpt": "chatgpt classic",
    "chat gpt": "chatgpt classic",
    "chatgpt": "chatgpt classic",
    "chrome": "google chrome",
    "edge": "microsoft edge",
    "edge": "msedge",
    "yt": "youtube",
    "youttube": "youtube",
    "utube": "youtube",
    "insta": "instagram",
    "ig": "instagram",
    "gemini": "google gemini",
    # Program
    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "code": "visual studio code",
    "idle": "idle (python 3.13 64-bit)",
    "python terminal": "python 3.13 (64-bit)",
    "git desktop": "github desktop",
    "git": "github desktop",
    # System-Apps
    "calc": "calculator",
    "note": "notepad",
    "notes": "notepad",
    "text editor": "notepad",
    "files": "file explorer",
    "explorer": "file explorer",
    "manager": "task manager",
    "tasks": "task manager",
    "control": "control panel",
    "store": "microsoft store",
    "bin": "recycle bin",
    "setting": "settings",
    "terminal": "terminal",
    "cmd": "command prompt",
    "command panel": "command prompt",
    # Applications
    "discord app": "discord",
    "whatsapp app": "whatsapp",
    "tele": "telegram",
    "tg": "telegram",
    # Media
    "steam client": "steam",
    "vlc": "vlc media player",
    "media player": "vlc media player",
    "gow": "god of war ragnarök",
    "god of war": "god of war ragnarök",
    "ragnarok": "god of war ragnarök",
    # Microsoft
    "word document": "word",
    "msword": "word",
    "ms word": "word",
    "paint": "mspaint",
    "powerpoint presentation": "powerpoint",
    "ppt": "powerpoint",
    "excel sheet": "excel",
    "msexcel": "excel",
}

COMMAND_ALIASES = {
    # OPEN
    "open": "open",
    "opn": "open",
    "launch": "open",
    "start": "open",
    "run": "open",
    "boot": "open",
    "execute": "open",
    "visit": "open",
    # SEARCH
    "search": "search",
    "find": "search",
    "google": "search",
    "lookup": "search",
    "browse": "search",
    "query": "search",
    # CLOSE
    "close": "close",
    "quit": "close",
    "exit": "close",
    "terminate": "close",
    "kill": "close",
    "shut": "close",
}


def normalize_target(target):
    """Normalize raw target text so aliases and process matching work reliably."""

    normalized = target.lower().strip()
    normalized = re.sub(r"[^a-z0-9\s]+", " ", normalized)
    normalized = " ".join(normalized.split())

    return TARGET_ALIASES.get(normalized, normalized)
