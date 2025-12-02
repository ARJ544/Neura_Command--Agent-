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
        
        what_to_write (str): Command to write in the specific terminal.
        
    Returns:
        Success or Error msg.
    """
    try:
        pyautogui.press("win")
        time.sleep(0.7)
        pyautogui.write(where_to_write)
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write(what_to_write, 0.1)
        
        return f"I had opened {where_to_write} and wrote {what_to_write}. User please press enter to execute."
    except Exception as e:
        return f"An error occured while writing : {e}"
