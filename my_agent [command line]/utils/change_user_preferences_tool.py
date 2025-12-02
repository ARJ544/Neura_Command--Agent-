"""Utility tool to change user preferences like name, Gemini API key, Tavily API key in the .env file."""

import os
from langchain.tools import tool

@tool
def change_user_preferences():
    """Tool used to remove/change user name and preference.
    """
     
    appdata = os.getenv("APPDATA")
    config_dir = os.path.join(appdata, "Neura Command")
    env_path = os.path.join(config_dir, ".env")

    
    if os.path.exists(env_path):
        os.remove(env_path)
        return "User preferences deleted successfully. Restart Application to set new preferences."
    else:
        return ".env file does not exist. Restart Application to create a new one."