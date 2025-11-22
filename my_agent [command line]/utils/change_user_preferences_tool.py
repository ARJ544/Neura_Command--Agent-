"""Utility tool to change user preferences like name, Gemini API key, Tavily API key in the .env file."""

import os
from langchain.tools import tool

@tool
def change_user_preferences(env_path: str):
    """Tool used to remove/change user name and preference. Ask user to give env_path (if they know) and say else default is ".env". Use ".env" if user don't know.
     Args:
         env_path (str): name of env file default is ".env".
     Returns:
         str: Confirmation message.
     """
     
    if os.path.exists(env_path):
        os.remove(env_path)
        return "User preferences deleted successfully. Restart Application to set new preferences."
    else:
        return ".env file does not exist. Restart Application to create a new one."
    