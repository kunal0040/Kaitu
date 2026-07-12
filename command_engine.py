import subprocess
import webbrowser
from urllib.parse import quote_plus

from app_registry import WEB_SITES
from app_discovery import get_installed_apps, close_application
from aliases import COMMAND_ALIASES, normalize_target

INSTALLED_APPS = get_installed_apps()


def open_application(app_name):
    app_name = app_name.lower().strip()

    web_url = WEB_SITES.get(app_name)
    app_id = INSTALLED_APPS.get(app_name)

    try:
        if app_id:
            subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])

        elif web_url:
            webbrowser.open(web_url)

        else:
            search_web(app_name)

        return f"Opening {app_name.title()}..."

    except Exception as error:
        return f"Failed to open {app_name.title()}. Error: {error}"


def search_web(search_query):

    encoded_query = quote_plus(search_query)
    search_url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(search_url)
    return f"Searching {search_query.title()}..."


def detect_command(user_input):
    normalized_input = user_input.lower().strip()

    parts = normalized_input.split(maxsplit=1)

    if len(parts) < 2:
        return None

    command = COMMAND_ALIASES.get(parts[0])
    target = parts[1]

    if not command:
        return None

    if command == "open":
        target = normalize_target(target)
        return {"command": "open_application", "target": target}

    elif command == "close":
        target = normalize_target(target)
        return {"command": "close_application", "target": target}

    elif command == "search":
        return {"command": "search_web", "target": target}

    return None


def execute_command(command_data):

    command = command_data["command"]
    target = command_data["target"]

    if command == "open_application":
        return open_application(target)

    elif command == "search_web":
        return search_web(target)

    elif command == "close_application":
        return close_application(target)

    return None
