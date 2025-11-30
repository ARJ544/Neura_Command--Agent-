"""
Tool to read content of a file.

Provided tool:
 - read_file: Read contents of a file
"""

import os
from typing import Literal
from langchain_core.tools import tool

EXCLUDED_EXTENSIONS = [
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".ico",
    ".mp3", ".wav", ".flac", ".aac", ".ogg",
    ".mp4", ".mkv", ".mov", ".avi", ".webm",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
    ".exe", ".dll", ".bin", ".dat", ".iso", ".apk",
    ".docx", ".xlsx", ".pptx", ".odt", ".ods"
]


BASE_DIR_MAP = {
    "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "Pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "Videos": os.path.join(os.path.expanduser("~"), "Videos"),
    "Music": os.path.join(os.path.expanduser("~"), "Music"),
    "Home": os.path.expanduser("~")
}

@tool
def read_file(name_of_file: str, base_dir: Literal["Desktop", "Documents", "Downloads", "Pictures","Videos", "Music", "Home"] = "Desktop"
):
    """
    Read the contents of a text file located inside a chosen base directory.
    Supports nested paths and automatically blocks binary/complex file types.

    Args:
        name_of_file (str):
            The file name or nested path to read.
            Examples:
                - "notes.txt"
                - "Projects/2025/plan.md"

        base_dir (str):
            The base directory where the file exists.
            Options:
                - Desktop
                - Documents
                - Downloads
                - Pictures
                - Videos
                - Music
                - Home

    Returns:
        str:
            - File content (if readable)
            - Error message (if something goes wrong)
    """

    full_path = os.path.join(BASE_DIR_MAP[base_dir], name_of_file)

    if not os.path.exists(full_path):
        return f"No file found at: {full_path}"

    file_extension = os.path.splitext(full_path)[1].lower()

    if file_extension in EXCLUDED_EXTENSIONS:
        return (
            f"Cannot read this file type: {file_extension} "
            "Reason: It's a binary or complex file (image/audio/video/archive/etc.)"
        )

    try:
        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    except UnicodeDecodeError:
        return "File contains binary data (not plain text). It may be corrupted or an unsupported format."
    
    except PermissionError:
        return "Permission denied! You don't have access to read this file."
    
    except Exception as e:
        return f"Unexpected error while reading file: {e}"
