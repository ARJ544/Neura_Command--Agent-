"""
Utility tools to create, rename, and delete files on the Desktop. Can also add text in existing/new file
provided tools:
 - create_add_content_file: Creates a new file on the Desktop and writes optional content. This tool can also be used to add content in existing file.
 - rename_file: Renames a file after asking user for confirmation.
 - delete_file: Moves a file to Recycle Bin after confirmation (Safe Delete).
"""
import os
from typing import Literal
from send2trash import send2trash
from langchain_core.tools import tool

@tool
def create_add_content_file(file_name: str, content: str = "", where_to_create: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop", inwhich_folder_to_create: str|None = None):
    """
    Creates a new file or updates an existing one inside a chosen base directory.
    If no file extension is detected, the user should be asked to provide one.
    This tool can also be used to write additional content into an existing file.

    Args:
        file_name (str):
            Name of the file, including its extension
            (e.g., "notes.txt", "script.py").
        
        content (str, optional):
            The text content to write into the file.
            If the file already exists, the content will replace the old content.
            Defaults to an empty string.

        where_to_create (str):
            Selects the base directory:
                - Desktop
                - Documents
                - Downloads
                - Pictures
                - Videos
                - Music
                - Home
                
        inwhich_folder_to_create (str|None, optional):
            (Optional) Specify a subfolder within the base directory
            where the file should be created.
            If None, the file is created directly in the base directory.
            Example: "Projects/2025/Notes"

    Returns:
        str: Success or error message.
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

    if "." not in file_name:
        return "Error: File extension missing. Please include a file extension such as .txt, .py, .json etc."
    if inwhich_folder_to_create:
        base_dir = os.path.join(base_dir, inwhich_folder_to_create)
        
    file_path = os.path.join(base_dir, file_name)
    normalized_path = os.path.normpath(file_path)

    try:
        with open(normalized_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File created or updated successfully at: {normalized_path}"
    except Exception as e:
        return f"Error creating or writing to file at {normalized_path}: {e}"

@tool
def rename_file(old_name: str, new_name: str, where_to_rename: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop"):
    """
    Renames an existing file inside a chosen base directory.
    File extensions must be included in both old and new names.
    
    Args:
        old_name (str):
            The current file name, including extension
            (e.g., "old_notes.txt").

        new_name (str):
            The new file name, including extension
            (e.g., "updated_notes.txt").

        where_to_rename (str):
            Base directory where the file exists:
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

    if "." not in old_name:
        return "Error: File extension missing in old_name. Please include a valid extension."

    if "." not in new_name:
        return "Error: File extension missing in new_name. Please include a valid extension."

    old_path = os.path.normpath(os.path.join(base_dir, old_name))
    new_path = os.path.normpath(os.path.join(base_dir, new_name))

    try:
        os.rename(old_path, new_path)
        return f"File renamed successfully from: {old_path} to: {new_path}"
    except FileNotFoundError:
        return f"Error: File not found at: {old_path}"
    except FileExistsError:
        return f"Error: A file already exists at: {new_path}"
    except Exception as e:
        return f"Error renaming file at {old_path}: {e}"

@tool
def delete_file(file_name: str, base_dir_of: Literal["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music", "Home"] = "Desktop"
):
    """
    Moves an existing file to the Recycle Bin inside a chosen base directory.
    File extension must be included in the file_name.

    Args:
        file_name (str):
            Name of the file to delete, including extension
            (e.g., "notes.txt", "image.png").

        base_dir_of (str):
            Base directory of the file:
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

    if base_dir_of == "Desktop":
        base_dir = os.path.join(home_dir, "Desktop")
    elif base_dir_of == "Documents":
        base_dir = os.path.join(home_dir, "Documents")
    elif base_dir_of == "Downloads":
        base_dir = os.path.join(home_dir, "Downloads")
    elif base_dir_of == "Pictures":
        base_dir = os.path.join(home_dir, "Pictures")
    elif base_dir_of == "Videos":
        base_dir = os.path.join(home_dir, "Videos")
    elif base_dir_of == "Music":
        base_dir = os.path.join(home_dir, "Music")
    elif base_dir_of == "Home":
        base_dir = home_dir

    if "." not in file_name:
        return "Error: File extension missing. Please include a valid extension such as .txt or .py"

    file_path = os.path.normpath(os.path.join(base_dir, file_name))

    try:
        send2trash(file_path)
        return f"File moved to Recycle Bin: {file_path}"
    except FileNotFoundError:
        return f"Error: No file found at: {file_path}"
    except Exception as e:
        return f"Error deleting file at {file_path}: {e}"
    
