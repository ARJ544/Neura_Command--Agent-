"""
Utility used to capture screen and get text from that.
Provided tools:
 - read_screen_text: Used to capture screen of next window.
"""

import os
import time
import uuid
import requests
from dotenv import load_dotenv
from PIL import ImageGrab
import pyautogui
from typing import Literal
from langchain_core.tools import tool

load_dotenv()
ocr_apikey = os.getenv("OCR_API_KEY")

if not ocr_apikey:
    with open(".env", 'a') as f:
        f.write(f"OCR_API_KEY={""}\n")
        print(f"OCR_API_KEY not found!!! Added OCR_API_KEY in .env\n")


OCR_LANGUAGES = {
    "English": "eng",
    "Arabic": "ara",
    "Bulgarian": "bul",
    "Chinese (Simplified)": "chs",
    "Chinese (Traditional)": "cht",
    "Croatian": "hrv",
    "Czech": "cze",
    "Danish": "dan",
    "Dutch": "dut",
    "Finnish": "fin",
    "French": "fre",
    "German": "ger",
    "Greek": "gre",
    "Hungarian": "hun",
    "Italian": "ita",
    "Japanese": "jpn",
    "Korean": "kor",
    "Polish": "pol",
    "Portuguese": "por",
    "Russian": "rus",
    "Slovenian": "slv",
    "Spanish": "spa",
    "Swedish": "swe",
    "Turkish": "tur",
    "Ukrainian": "ukr",
    "Vietnamese": "vnm"
}

SupportedLanguage = Literal[
    "English", "Arabic", "Bulgarian", "Chinese (Simplified)", "Chinese (Traditional)",
    "Croatian", "Czech", "Danish", "Dutch", "Finnish", "French", "German",
    "Greek", "Hungarian", "Italian", "Japanese", "Korean", "Polish",
    "Portuguese", "Russian", "Slovenian", "Spanish", "Swedish", "Turkish",
    "Ukrainian", "Vietnamese"
]

@tool
def read_screen_text(which_screen: int, language: SupportedLanguage = "English"):
    """
    Reads text from a window on the user's computer using OCR.

    WHEN THE AGENT SHOULD CALL THIS TOOL:
        - Call this tool whenever the user asks to "read", "check", "see",
          "look at", "analyze", or "find the text" from their screen.
        - Call this tool when the user mentions that an error message,
          code snippet, popup, warning, or any text is visible on their screen.
        - If the user says things like:
              "There is an error on my screen"
              "Read the text on my window"
              "What does my screen say?"
              "Check what's displayed"
              "Look at the message I see"
          → The agent MUST call this tool automatically.

    WHAT THE TOOL DOES:
        - Optionally switches to another window using Alt+Tab.
        - Captures a screenshot.
        - Extracts text from it.
        - Returns the extracted text.

    Args:
        which_screen (int): Specifies which screen to capture in the screenshot. Ask before invoking.
            - If 1, captures the current screen (Agent).  
            - If 2, simulates pressing Alt+Tab once to move to the next screen before capturing.  
            - If 3, simulates pressing Alt+Tab twice to reach the screen after next, and so on.  
            Essentially, the value represents either the screen index or the number of Alt+Tab presses required.

    
        language (str): Language of the text to extract. 
            Must be one of the supported languages. Default is "English".
            options: [
                "English", "Arabic", "Bulgarian", "Chinese (Simplified)", "Chinese (Traditional)",
                "Croatian", "Czech", "Danish", "Dutch", "Finnish", "French", "German",
                "Greek", "Hungarian", "Italian", "Japanese", "Korean", "Polish",
                "Portuguese", "Russian", "Slovenian", "Spanish", "Swedish", "Turkish",
                "Ukrainian", "Vietnamese"
            ]

    Returns:
        str: Extracted text from the screen, or an error message if OCR fails or
        an exception occurs.
    """
    try:
        if which_screen < 1:
            return "which_screen must be >= 1"
        
        ocr_language_code = OCR_LANGUAGES[language]
        
        if which_screen > 1:
            pyautogui.keyDown('alt')
            for _ in range(which_screen - 1):
                pyautogui.press('tab')
            pyautogui.keyUp('alt')


        time.sleep(0.7)
        
        file_name = f"screenshot_{uuid.uuid4()}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(file_name)
        
        if not which_screen == 1:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')

        
        api_url = "https://api.ocr.space/parse/image"
        with open(file_name, "rb") as f:
            response = requests.post(
                api_url,
                files={"filename": f},
                data={"apikey": ocr_apikey, "language": ocr_language_code}
            )

        os.remove(file_name)

        result = response.json()
        if result.get("IsErroredOnProcessing"):
            return f"OCR Error: {result.get('ErrorMessage', 'Unknown error')}"

        extracted_text = result["ParsedResults"][0]["ParsedText"]
        return extracted_text.strip()

    except Exception as e:
        return f"Exception occurred: {str(e)}"
