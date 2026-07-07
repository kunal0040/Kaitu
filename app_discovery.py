import subprocess
import json


def get_installed_apps():

    result = subprocess.run(
        ["Powershell", "-Command", "Get-StartApps | ConvertTo-Json"],
        capture_output=True,
        text=True,
    )

    try:
        apps = json.loads(result.stdout)
    
    except (json.JSONDecodeError, TypeError):
        return {}

    installed_apps = {}

    for app in apps:
        name = app["Name"]
        app_id = app["AppID"]

        norm_name = name.lower().strip()
        installed_apps[norm_name] = app_id

    return installed_apps
