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
def read_screen_text(language: SupportedLanguage = "English"):
    """
    Captures a screenshot of the currently active window (excluding the agent window)
    and extracts text using OCR. Temporarily switches windows using Alt+Tab to
    access the target screen.

    Notes:
    - Designed for automation tasks where screen content needs to be read.
    - Returns the extracted text as a string.

    Args:
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
        # Get OCR code from language
        ocr_language_code = OCR_LANGUAGES[language]

        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.keyUp('alt')

        time.sleep(0.8)
        
        file_name = f"screenshot_{uuid.uuid4()}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(file_name)
        
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
