"""
Tools to create, rename, and delete folders.
provided tools:
 - create_folder: Creates a new folder at the specified path.
 - rename_folder: Renames an existing folder to a new name.
 - delete_folder: Deletes the specified folder.
"""

from langchain_core.tools import tool
from typing import Literal
import os
from send2trash import send2trash

@tool
def create_folder(name_of_folder: str, where_to_create: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop"):
    
    """
    Create a new folder (including nested subfolders) in a chosen directory inside the user's home. Ask user to confirm the target location before creating anything.

    This function first confirms the target location before creating anything.  
    It supports both simple folder names and nested structures, such as:
        "ProjectA/UI/Components/Buttons".

    Args:
        name_of_folder (str):
            The folder name or nested folder path to create.
            Use forward slashes to define subfolders.
            Example:
                "NewFolder"
                "Work/2025/Reports/Images"

        where_to_create (str):
            The base location where the folder should be created.
            Accepted values:
                - "Desktop"
                - "Documents"
                - "Downloads"
                - "Pictures"
                - "Videos"
                - "Music"
                - "Home" : Home dir is "C:\\Users\\<name>"

    Returns:
        str:
            A message indicating whether the folder creation succeeded or if an error occurred.
    """
    home_dir = os.path.expanduser("~")

    if where_to_create == "Desktop":
        base_dir = os.path.join(home_dir, "Desktop")
    elif where_to_create == "Documents":
        base_dir = os.path.join(home_dir, "Documents")
    elif where_to_create == "Downloads":
        base_dir = os.path.join(home_dir, "Downloads")
    elif where_to_create == "Pictures":
        base_dir = os.path.join(home_dir, "Pictures")
    elif where_to_create == "Videos":
        base_dir = os.path.join(home_dir, "Videos")
    elif where_to_create == "Music":
        base_dir = os.path.join(home_dir, "Music")
    elif where_to_create == "Home":
        base_dir = home_dir
        
    folder_path = os.path.join(base_dir, name_of_folder)
    normalized_path = os.path.normpath(folder_path)
    
    try:
        os.makedirs(normalized_path, exist_ok=False)
        return f"Folder created successfully at: {normalized_path}"
    except FileExistsError:
        return f"Error: A folder already exists at: {normalized_path}"
    except Exception as e:
        return f"Error creating folder at {normalized_path}: {e}"

@tool
def rename_folder(current_name: str, new_name: str, where_to_rename: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop"
):
    """
    Renames an existing folder inside a chosen base directory. 
    Supports nested folder paths for both current and new names.

    Args:
        current_name (str):
            The current folder name or nested path (e.g., "Old/2024/Files").

        new_name (str):
            The new folder name or nested path (e.g., "New/2024/Files").

        where_to_rename (str):
            Base directory where the folder exists:
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
    home_dir = os.path.expanduser("~")


    if where_to_rename == "Desktop":
        base_dir = os.path.join(home_dir, "Desktop")
    elif where_to_rename == "Documents":
        base_dir = os.path.join(home_dir, "Documents")
    elif where_to_rename == "Downloads":
        base_dir = os.path.join(home_dir, "Downloads")
    elif where_to_rename == "Pictures":
        base_dir = os.path.join(home_dir, "Pictures")
    elif where_to_rename == "Videos":
        base_dir = os.path.join(home_dir, "Videos")
    elif where_to_rename == "Music":
        base_dir = os.path.join(home_dir, "Music")
    elif where_to_rename == "Home":
        base_dir = home_dir

    current_path = os.path.normpath(os.path.join(base_dir, current_name))
    new_path = os.path.normpath(os.path.join(base_dir, new_name))

    try:
        os.rename(current_path, new_path)
        return f"Folder renamed successfully from: {current_path} to: {new_path}"
    except FileNotFoundError:
        return f"Error: The folder does not exist at: {current_path}"
    except FileExistsError:
        return f"Error: A folder already exists at: {new_path}"
    except Exception as e:
        return f"Error renaming folder at {current_path}: {e}"
 
@tool
def delete_folder(name_of_folder: str, where_to_delete: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop"):
    """
    Deletes a folder or nested folder structure from a selected base directory
    and sends it to the Recycle Bin. Ask user before deleting.

    This function supports both simple folder names and nested paths such as:
        "ProjectA/2025/UI"
        "Work/Reports/Images"

    A folder is removed safely using send2trash, ensuring it can be recovered
    from the Recycle Bin instead of being permanently deleted.

    Args:
        name_of_folder (str):
            The folder name or nested folder path to delete.
            Use forward slashes for subfolders.
            Examples:
                "MyFolder"
                "Projects/2025/Designs"

        where_to_delete (str):
            The base directory where the folder is located.
            Accepted values:
                - "Desktop"
                - "Documents"
                - "Downloads"
                - "Pictures"
                - "Videos"
                - "Music"
                - "Home"  (User's home directory: C:\\Users\\<name>)

    Returns:
        str:
            A message indicating whether the folder was successfully deleted
            or if an error occurred (e.g., folder not found).
    """
    home_dir = os.path.expanduser("~")

    if where_to_delete == "Desktop":
        base_dir = os.path.join(home_dir, "Desktop")
    elif where_to_delete == "Documents":
        base_dir = os.path.join(home_dir, "Documents")
    elif where_to_delete == "Downloads":
        base_dir = os.path.join(home_dir, "Downloads")
    elif where_to_delete == "Pictures":
        base_dir = os.path.join(home_dir, "Pictures")
    elif where_to_delete == "Videos":
        base_dir = os.path.join(home_dir, "Videos")
    elif where_to_delete == "Music":
        base_dir = os.path.join(home_dir, "Music")
    elif where_to_delete == "Home":
        base_dir = home_dir

    folder_path = os.path.join(base_dir, name_of_folder)
    normalized_path = os.path.normpath(folder_path)

    try:
        send2trash(normalized_path)
        return f"Folder deleted successfully at: {normalized_path}"
    except FileNotFoundError:
        return f"Error: No folder found at: {normalized_path}"
    except OSError as e:
        return f"Error deleting folder at {normalized_path}: {e}"
