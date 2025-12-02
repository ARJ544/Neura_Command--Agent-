import os
from utils import change_user_preferences_tool as cup
from utils import research_tools
from utils import open_close_min_max_res_apps_tool as ocmmr
from utils import control_brightness_volume_tool as cbv
from utils import create_rename_delete_folder_tool as crdf
from utils import create_rename_delete_file_tool as crdfile
from utils import move_file_folder as mff
from utils import create_or_extract_zip_tool as cez
from utils import read_file_tool as rft
from utils import open_url_query_in_browser_tool as ouqb
from utils import read_screen_text_tool as rst
from utils import terminal_control_tool as tst
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from InquirerPy import inquirer

load_dotenv()

ENV_PATH = ".env"
gemini_key = os.getenv("GOOGLE_API_KEY")
name = os.getenv("NAME")

if not gemini_key:
    while True:
        gemini_key = input("Enter your Gemini API: ").strip()
        if gemini_key:
            break
    with open(ENV_PATH, 'a') as f:
        f.write(f"GOOGLE_API_KEY={gemini_key}\n")
        print(f"Gemini_Api_Key not found!!! Added GOOGLE_API_KEY={gemini_key} in .env\n")     
if not name:
    while True:
        name = input("Enter your Name: ").strip()
        if name:
            break
    with open(ENV_PATH, 'a') as f:
        f.write(f"NAME={name}\n")
        print(f"NAME not found!!! Added NAME={name} in .env\n")
else:
    print(f"Gemini_Api_Key found!!! name = {name} gemini_key = {gemini_key}\n")


llm_choice = inquirer.select(
    message="Choose an LLM (Use Arrow keys) to select:",
    choices=[
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro"
], 
    qmark = "",
    long_instruction="Choose fast 😁"
).execute()
# LLM
llm = ChatGoogleGenerativeAI(
    model=llm_choice,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=0,
    google_api_key=gemini_key,
)
tools = [research_tools.internet_search, research_tools.web_scraper, ocmmr.open_app, ocmmr.close_app, ocmmr.minimize_app, ocmmr.maximize_app, ocmmr.restore_app, ocmmr.switch_btwn_apps, cbv.set_volume, cbv.set_brightness, crdf.create_folder, crdf.rename_folder, crdf.delete_folder, crdfile.create_add_content_file, crdfile.rename_file, crdfile.delete_file, mff.move_file_folder, cez.create_zipfile, cez.extract_zipfile, rft.read_file, ouqb.open_url_or_query, rst.read_screen_text, tst.write_command_in_terminal, cup.change_user_preferences]
tools_by_name = {tool.name: tool for tool in tools}
llmwithtools = llm.bind_tools(tools)