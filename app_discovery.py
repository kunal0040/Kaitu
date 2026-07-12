import subprocess
import json
import pygetwindow as gw
from aliases import normalize_target


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
        name = app.get("Name")
        app_id = app.get("AppID")

        if name and app_id:
            norm_name = name.lower().strip()
            installed_apps[norm_name] = app_id

    return installed_apps


def get_running_process():
    result = subprocess.run(
        [
            "Powershell",
            "-Command",
            "Get-Process | Select-Object ProcessName | ConvertTo-Json",
        ],
        capture_output=True,
        text=True,
    )

    try:
        processes = json.loads(result.stdout)
    except (json.JSONDecodeError, TypeError):
        return {}

    running_processes = {}

    for process in processes:
        process_name = process.get("ProcessName")

        if process_name:
            normalized_name = process_name.lower().strip()
            running_processes[normalized_name] = process_name

    return running_processes


def close_application(app_name):
    app_name = normalize_target(app_name)

    open_windows = gw.getAllWindows()

    for window in open_windows:
        window_title = window.title.lower().strip()

        if window_title and app_name in window_title:
            window.close()
            return f"{app_name.title()} Closed."

    running_processes = get_running_process()
    process_name = running_processes.get(app_name)

    if not process_name:

        for running_app in running_processes.values():
            if app_name in running_app.lower():
                process_name = running_app
                break

    if not process_name:
        return f"I couldn't find a running process for {app_name.title()}."

    try:
        result = subprocess.run(
            ["taskkill", "/IM", f"{process_name}.exe", "/F"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return f"Closed {app_name.title()}."

        return f"I couldn't close {app_name.title()}"

    except Exception as error:
        return f"Failed to close {app_name.title()}. Error: {error}"
