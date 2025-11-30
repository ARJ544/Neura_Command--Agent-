"""
Utility tools for working with ZIP archives.
Provided tools:
 - extract_zipfile: Extract an existing ZIP file into a selected directory.
 - create_zipfile: Create a ZIP archive from an existing folder or file into a selected directory.
"""

import os
import shutil
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
def extract_zipfile(
    zip_file_path: str,
    extract_to: str,
    base_dir_of_zip: Literal["Desktop","Documents","Downloads","Pictures","Videos","Music","Home"] = "Desktop",
    base_dir_of_extract_to: Literal["Desktop","Documents","Downloads","Pictures","Videos","Music","Home"] = "Desktop"
):
    """
    Extract a ZIP file from a chosen base directory to another chosen base directory.
    Supports nested folder paths.

    Args:
        zip_file_path (str):
            Name or nested path of the zip file (e.g., "MyZips/archive.zip"). with extension.

        extract_to (str):
            Folder or nested path where the contents will be extracted.
            Will be created automatically if missing.

        base_dir_of_zip (str):
            Base directory where zip_file_path exists.
                - Desktop
                - Documents
                - Downloads
                - Pictures
                - Videos
                - Music
                - Home

        base_dir_of_extract_to (str):
            Base directory where extract_to will be created.
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
    if not zip_file_path.lower().endswith(".zip"):
        zip_file_path+= ".zip"

    base_zip_dir = resolve_base_dir(base_dir_of_zip)
    base_extract_dir = resolve_base_dir(base_dir_of_extract_to)

    # Full paths
    zip_path = os.path.normpath(os.path.join(base_zip_dir, zip_file_path))
    extract_path = os.path.normpath(os.path.join(base_extract_dir, extract_to))

    try:
        if not os.path.exists(zip_path):
            return f"Error: ZIP file does not exist at: {zip_path}"

        shutil.unpack_archive(zip_path, extract_path, 'zip')
        return f"Extracted successfully from '{zip_path}' to '{extract_path}'"

    except shutil.ReadError:
        return f"Error: The file at '{zip_path}' is not a valid ZIP archive."

    except Exception as e:
        return f"Error extracting ZIP: {e}"

@tool
def create_zipfile(
    folder_to_zip: str,
    zip_file_name: str,
    base_dir_of_folder: Literal["Desktop","Documents","Downloads","Pictures","Videos","Music","Home"] = "Desktop",
    base_dir_of_zip: Literal["Desktop","Documents","Downloads","Pictures","Videos","Music","Home"] = "Desktop"
):
    """
    Create a ZIP file from a chosen base directory and save it to another chosen base directory.
    Supports nested folder paths.

    Args:
        folder_to_zip (str):
            Folder name or nested path to be zipped (e.g., "Work/2025/Projects").

        zip_file_name (str):
            Name of the zip file to create. Must include .zip extension.
            If user forgets, .zip will be added automatically.

        base_dir_of_folder (str):
            Base directory where folder_to_zip exists:
                - Desktop
                - Documents
                - Downloads
                - Pictures
                - Videos
                - Music
                - Home

        base_dir_of_zip (str):
            Base directory where the resulting ZIP file will be saved:
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

    base_folder_dir = resolve_base_dir(base_dir_of_folder)
    base_zip_dir = resolve_base_dir(base_dir_of_zip)

    # Full paths
    source_folder = os.path.normpath(os.path.join(base_folder_dir, folder_to_zip))
    zip_path = os.path.normpath(os.path.join(base_zip_dir, zip_file_name))

    # Automatically append .zip if user forgot
    if not zip_path.lower().endswith(".zip"):
        zip_path += ".zip"

    try:
        
        if not os.path.exists(source_folder):
            return f"Error: The folder you want to zip does not exist: {source_folder}"

        zip_base, _ = os.path.splitext(zip_path)

        root_dir = os.path.dirname(source_folder)
        base_dir = os.path.basename(source_folder)

        shutil.make_archive(zip_base, 'zip', root_dir=root_dir, base_dir=base_dir)

        return f"Created ZIP successfully at: {zip_path}"

    except Exception as e:
        return f"Error creating ZIP: {e}"
