"""
Tools to create, rename, and delete folders.
provided tools:
 - create_folder: Creates a new folder at the specified path.
 - rename_folder: Renames an existing folder to a new name.
 - delete_folder: Deletes the specified folder.
"""

from langchain_core.tools import tool
import os
from send2trash import send2trash

@tool
def create_folder(name_of_folder: str):
    """
    Creates a new folder or folder in folder at Desktop directory with the specified name of folder.

    Args:
        name_of_folder (str): The name of folder or folder in folder to be created. It can include subfolder names separated by forward slashes (e.g., "NewFolder/xyz/yz/as/pi").

    Returns:
        str: Success or error message.
    """
    home_dir = os.path.expanduser("~")
    desktop_dir = os.path.join(home_dir, "Desktop")
    folder_path = os.path.join(desktop_dir, name_of_folder)
    normalized_path = os.path.normpath(folder_path)
    try:
        os.makedirs(normalized_path, exist_ok=False)
        return f"Folder created successfully at: {normalized_path}"
    except FileExistsError:
        return f"Error: A folder already exists at: {normalized_path}"
    except Exception as e:
        return f"Error creating folder at {normalized_path}: {e}"

@tool
def rename_folder(current_name: str, new_name: str):
    """
    Renames an existing folder on the Desktop after asking user for confirmation.

    Args:
        current_name (str): The current name of the folder to be renamed. It can include subfolder names separated by forward slashes (e.g., "OldFolder/xyz").
        new_name (str): The new name for the folder. It can include subfolder names separated by forward slashes (e.g., "NewFolder/abc").

    Returns:
        str: Success or error message.
    """
    home_dir = os.path.expanduser("~")
    desktop_dir = os.path.join(home_dir, "Desktop")
    current_path = os.path.normpath(os.path.join(desktop_dir, current_name))
    new_path = os.path.normpath(os.path.join(desktop_dir, new_name))
    try:
        os.rename(current_path, new_path)
        return f"Folder renamed successfully from {current_path} to {new_path}"
    except FileNotFoundError:
        return f"Error: The folder '{current_path}' does not exist."
    except FileExistsError:
        return f"Error: A folder with the name '{new_path}' already exists."
    except Exception as e:
        return f"Error renaming folder: {e}"
    
@tool
def delete_folder(name_of_folder: str):
    """
    Removes and send an existing folder or folder in folder from Desktop directory to Recycle Bin with the specified name of folder after asking for confirmation. [Do you want to delete <folder_name>?]

    Args:
        name_of_folder (str): The name of folder or folder in folder to be deleted. It can include subfolder names separated by forward slashes (e.g., "NewFolder/xyz/yz/as/pi").

    Returns:
        str: Success or error message.
    """
    home_dir = os.path.expanduser("~")
    desktop_dir = os.path.join(home_dir, "Desktop")
    folder_path = os.path.join(desktop_dir, name_of_folder)
    normalized_path = os.path.normpath(folder_path)
    try:
        send2trash(normalized_path)
        return f"Folder deleted successfully at: {normalized_path}"
    except FileNotFoundError:
        return f"Error: No folder found at: {normalized_path}"
    except OSError as e:
        return f"Error deleting folder at {normalized_path}: {e}"