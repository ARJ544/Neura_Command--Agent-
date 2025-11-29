"""
Utility tool to move files/folder.
provided tools:
 - move_file_folder: Move existing file/folder to existing file/folder.
"""

import shutil
import os
from typing import Literal
from langchain_core.tools import tool
    
BASE_DIRS = {
    "Desktop": "Desktop",
    "Documents": "Documents",
    "Downloads": "Downloads",
    "Pictures": "Pictures",
    "Videos": "Videos",
    "Music": "Music",
    "Home": "",
}

def resolve_base_dir(base: str) -> str:
    home = os.path.expanduser("~")
    sub = BASE_DIRS.get(base, "")
    return os.path.join(home, sub) if sub else home

@tool
def move_file_folder(current_name: str, new_destination_path: str, base_dir_of_destination: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop", base_dir_of_current_name: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop"
):
    """
    Move an existing folder/file inside a chosen base directory. 
    Supports nested folder paths for both current and destination names.

    Args:
        current_name (str):
            The current folder/file name or nested path (e.g., "Old/2025/Files").

        new_destination_path (str):
            The destination where the file will be created name or nested path (e.g., "New/2025/Files").
            Can be empty string "" if want to move to base_dir_of_destination

        base_dir_of_destination (str):
            Base directory where the new_destination_path exists:
                - Desktop
                - Documents
                - Downloads
                - Pictures
                - Videos
                - Music
                - Home
        
        base_dir_of_current_name (str):
            Base directory where the current_name exists:
                - Desktop
                - Documents
                - Downloads
                - Pictures
                - Videos
                - Music
                - Home

    Returns:
        str: Success or error message.
    """
        
    base_dir_of_current_name = resolve_base_dir(base_dir_of_current_name)
    base_dir_of_destination = resolve_base_dir(base_dir_of_destination)

    current_path = os.path.normpath(os.path.join(base_dir_of_current_name, current_name))
    new_path = os.path.normpath(os.path.join(base_dir_of_destination, new_destination_path))

    try:
        if not os.path.exists(new_path):
            return f"The destination path {new_path} doesn't exists. Try creating new one."
        shutil.move(current_path, new_path)
        return f"Moved successfully from: {current_path} to: {new_path}"
    except FileNotFoundError as e:
        return f"Error: The Path does not exist : {current_path}. Try creating new one."
    except FileExistsError:
        return f"Error: Already exists at: {new_path}"
    except Exception as e:
        return f"Error moving at {current_path}: {e}"
