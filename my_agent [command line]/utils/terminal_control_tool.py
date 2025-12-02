"""
Utility used to Execute commands in terminal.
Provided tools:
 - write_command_in_terminal: Write the command in [Powershell or CMD or Termianl]
"""

from langchain_core.tools import tool
from typing import Literal
import pyautogui, time

@tool
def write_command_in_terminal(where_to_write: Literal["Powershell", "Command Prompt", "Termianl"], what_to_write:str):
    """
    This tool is used to write command, script or anything in the "Powershell" or "Command Prompt" or "Termianl".
    Args:
        where_to_write (Literal): Choose where to write the command. In "Powershell" or "Command Prompt" or "Termianl".
        
        what_to_write (str):
            The exact command to write in the terminal. Any valid system
            command, script, CLI instruction, or shell expression can be
            provided here.
            
            Additionally, if the user describes an action in natural language
            (e.g., "create a new directory", "show my Python version",
            "list all files"), this tool will convert that description into the
            appropriate command and execute it on their behalf.
        
    Returns:
        Success or Error msg.
    """
    try:
        pyautogui.press("win")
        time.sleep(0.7)
        pyautogui.write(where_to_write)
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.write(what_to_write, 0.1)
        
        return f"I had opened {where_to_write} and wrote {what_to_write}. User please press enter to execute. Also tell user what this command can do."
    except Exception as e:
        return f"An error occured while writing : {e}"
