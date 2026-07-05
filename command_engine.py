import os
import webbrowser

APPLICATIONS = {
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "calculator": "calc.exe",
    "youtube": r"C:\Users\Kunal Bhargav\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Brave Apps\YouTube.lnk"
}

WEB_APPS = {
    "google": "https://www.google.com",
    "github": "https://www.github.com"
}

def open_application(app_name):
    app_path = APPLICATIONS.get(app_name.lower())
    web_url = WEB_APPS.get(app_name.lower())

    if not web_url and not app_path:
        return f"Sorry, I'm unable to open {app_name.title()}"

    try:
        if app_path:
            os.startfile(app_path)
        
        elif web_url:
            webbrowser.open(web_url)
        
        return f"Opening {app_name.title()}..."
    
    except Exception as error:
        return f"Failed to open {app_name.title()}. Error: {error}"


def detect_command(user_input):
    normalized_input = user_input.lower().strip()

    if normalized_input.startswith("open "):
        app_name = normalized_input.removeprefix("open ").strip()
        return {"command": "open_application", "target": app_name}
    return None


def execute_command(command_data):
    command = command_data["command"]
    target = command_data["target"]

    if command == "open_application":
        return open_application(target)
    return None
