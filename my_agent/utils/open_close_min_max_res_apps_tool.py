import os
import subprocess, time, pyautogui
from pathlib import Path
from langchain_core.tools import tool
import pygetwindow as gw
# import difflib
from rapidfuzz import process, fuzz

def get_all_file_paths_and_names(directory_path):
    """
    Gets the full path and the name (without extension) of all files 
    in the specified directory and its subdirectories using pathlib.

    Returns:
        A list of dictionaries, where each dictionary contains:
        - 'path': The full absolute path string.
        - 'name': The file name without the extension.
    """
    path = Path(directory_path)
    file_data = []

    for item in path.glob('**/*'):
        if item.is_file():
            # Get the full absolute path as a string
            full_path = str(item.resolve()) 
            
            # Get the file name without the extension
            name_without_ext = item.stem.lower()
            
            file_data.append({
                'path': full_path,
                'name': name_without_ext
            })

    return file_data

directory = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs'
directory2 = f"{os.path.expanduser('~')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"

@tool
def open_app(window_name: str):
    """
    Opens a Windows application by any provided name. Valid and invalid both names are allowed.

    Args:
        window_name (str): Name of any app or executable.

    Returns:
        str: Success or error message.
    """
    all_apps_data = get_all_file_paths_and_names(directory)
    extra_apps = get_all_file_paths_and_names(directory2)
    all_apps_data.extend(extra_apps)


    appname = [app['name'] for app in all_apps_data]
    app_paths = [app['path'] for app in all_apps_data]


    names_lower = [name.lower() for name in appname]

    match = process.extractOne(
        window_name.lower(),
        names_lower,
        scorer=fuzz.partial_ratio
    )

    if match is None or match[1] < 70:
        pyautogui.press("win")
        time.sleep(1)
        pyautogui.write(window_name)
        return f"{window_name} was not an application, so it was searched in the Windows search bar."

    
    matched_name_lower = match[0]


    index = names_lower.index(matched_name_lower)

    final_path = app_paths[index]
    original_name = appname[index]

    try:
        subprocess.Popen(final_path, shell=True)
        return f"'{original_name}' has been opened successfully."
    except Exception as e:
        return f"Failed to open '{original_name}': {e}"


def find_closest_window_title(query : str):
    """
    From active windows applications get the most closest app name
    """
    titles = gw.getAllTitles()
    result = process.extractOne(query, titles, scorer=fuzz.partial_ratio)
    return result[0] if result else None

@tool
def close_app(window_name: str):
    """
    Closes the desktop application window.

    Args:
        window_name (str): The title/name (full or partial) of the window
        you want to close.

    Returns:
        str: Confirmation message indicating whether the matching
        window was successfully closed or not found.
    """
    window_to_close = find_closest_window_title(window_name)
    if window_to_close:
        window_handle = gw.getWindowsWithTitle(window_to_close)[0]
        window_handle.close()
        return f"{window_to_close} was closed "
    else:
        return f"No window found with a title close to '{window_name}'"
    
@tool
def minimize_app(window_name: str):
    """
    Minimizes the desktop window.

    Args:
        window_name (str): The full or partial title/name of the window
        you want to minimize.

    Returns:
        str: Message indicating whether the matching window was
        successfully minimized or not found.
    """
    window_to_minimize = find_closest_window_title(window_name)
    if window_to_minimize:
        window_handle = gw.getWindowsWithTitle(window_to_minimize)[0]
        window_handle.minimize()
        return f"{window_to_minimize} was minimized "
    else:
        return f"No window found with a title close to '{window_name}'"

@tool
def maximize_app(window_name: str):
    """
    Maximizes the desktop window.

    Args:
        window_name (str): The full or partial title/name of the window
        you want to maximize.

    Returns:
        str: Message indicating whether the matching window was
        successfully maximized or not found.
    """
    window_to_maximize = find_closest_window_title(window_name)
    if window_to_maximize:
        window_handle = gw.getWindowsWithTitle(window_to_maximize)[0]
        window_handle.maximize()
        window_handle.activate()
        return f"{window_to_maximize} was maximized "
    else:
        return f"No window found with a title close to '{window_name}'"

@tool
def restore_app(window_name: str):
    """
    Restores a minimized or maximized desktop window.

    Args:
        window_name (str): The full or partial title/name of the window
        you want to restore.

    Returns:
        str: Message indicating whether the matching window was
        successfully restored or not found.
    """
    window_to_restore = find_closest_window_title(window_name)
    if window_to_restore:
        window_handle = gw.getWindowsWithTitle(window_to_restore)[0]
        window_handle.restore()
        return f"{window_to_restore} was restored "
    else:
        return f"No window found with a title close to '{window_name}'"

@tool
def switch_btwn_apps(window_name: str):
    """
    Switch between apps just like alt+tab.

    Args:
        window_name (str): The full or partial title/name of the window app
        you want to switch to.

    Returns:
        str: Message indicating whether the matching window was
        successfully switched or not found.
    """
    window_to_switch = find_closest_window_title(window_name)
    if window_to_switch:
        window_handle = gw.getWindowsWithTitle(window_to_switch)[0]
        if not window_handle.isMaximized:
            window_handle.restore()
            window_handle.activate()
            return f"{window_to_switch} is active now. "
        else:
            window_handle.activate()
            return f"{window_to_switch} is active now. "
    else:
        return f"No window found with a title '{window_name}' to switch to."
