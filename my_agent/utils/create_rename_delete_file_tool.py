"""
Utility tools to create, rename, and delete files on the Desktop.
provided tools:
 - create_add_content_file: Creates a new file on the Desktop and writes optional content. This tool can also be used to add content in existing file.
 - rename_file: Renames a file after asking user for confirmation.
 - delete_file: Moves a file to Recycle Bin after confirmation (Safe Delete).
"""
import os
from send2trash import send2trash
from langchain_core.tools import tool

@tool
def create_add_content_file(file_name: str, content: str = ""):
    """
    Creates a new file on the Desktop and writes optional content. Ask to enter file extension if not provided in file_name. Also ask if something to write in the file. This tool can also be used to add content in existing file.
    
    Args:
        file_name (str): The name of the file to be created. It should include the file extension (e.g., "example.txt").
        content (str, optional): The content to write into the file. Defaults to an empty string.
        
    Returns:
        str: Success or error message.
    """

    home_dir = os.path.expanduser("~")
    desktop_dir = os.path.join(home_dir, "Desktop")
    file_path = os.path.join(desktop_dir, file_name)
    normalized_path = os.path.normpath(file_path)

    try:
        with open(normalized_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File created successfully at: {normalized_path} with content = '{content}'"
    except Exception as e:
        return f"Error creating file: {e}"
    
@tool
def rename_file(old_name: str, new_name: str):
    """
    Renames a file after asking user for confirmation. Asks to enter file extensions if not provided in old_name or new_name.
    Args:
        old_name (str): The current name of the file to be renamed. It should include the file extension (e.g., "old_example.txt").
        new_name (str): The new name for the file. It should include the file extension (e.g., "new_example.txt").
    Returns:
        str: Success or error message.
    """

    home_dir = os.path.expanduser("~")
    desktop = os.path.join(home_dir, "Desktop")

    old_path = os.path.normpath(os.path.join(desktop, old_name))
    new_path = os.path.normpath(os.path.join(desktop, new_name))

    try:
        os.rename(old_path, new_path)
        return f"Renamed successfully:\nFROM: {old_path}\nTO:   {new_path}"
    except Exception as e:
        return f"Error renaming: {e}"

@tool
def delete_file(file_name: str):
    """
    Moves a file to Recycle Bin after confirmation (Safe Delete).
    
    Args:
        file_name (str): The name of the file to be deleted.
    Returns:
        str: Success or error message.
    """

    home_dir = os.path.expanduser("~")
    desktop = os.path.join(home_dir, "Desktop")
    file_path = os.path.normpath(os.path.join(desktop, file_name))

    try:
        send2trash(file_path)
        return f"File moved to Recycle Bin: {file_path}"
    except Exception as e:
        return f"Error deleting file: {e}"
