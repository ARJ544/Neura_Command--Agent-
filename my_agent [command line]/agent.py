import warnings
warnings.filterwarnings(
    "ignore", 
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater."
)

from utils import change_user_preferences_tool as cup
from utils import research_tools
from utils import open_close_min_max_res_apps_tool as ocmmr
from utils import control_brightness_volume_tool as cbv
from utils import create_rename_delete_folder_tool as crdf
from utils import create_rename_delete_file_tool as crdfile
from langgraph.graph import StateGraph, MessagesState, START, END
import os, threading
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core import exceptions
from langchain_core.messages import HumanMessage,SystemMessage, ToolMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from colorama import Fore, Style, init
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
init(autoreset=True)
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

def clear_gemini_api(env_path):
    if not os.path.exists(env_path):
        print(Fore.RED + "Wrong API key will be deleted from .env")
        print(Fore.RED + "Your luck!!! No .env file found. Restart App.")
        return
    
    with open(env_path, "r") as f:
        lines = f.readlines()
    new_lines = [line for line in lines if not line.startswith("GOOGLE_API_KEY")]

    if len(new_lines) == len(lines):
        print(Fore.RED + "GOOGLE_API_KEY not found in .env. May be deleted before!")
        return

    with open(env_path, "w") as f:
        f.writelines(new_lines)

    print(Fore.RED + "GOOGLE_API_KEY removed from .env successfully due to invalid API KEY! Restart App to enter valid api key.")

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=0,
    google_api_key=gemini_key,
)
tools = [research_tools.internet_search, research_tools.web_scraper, ocmmr.open_app, ocmmr.close_app, ocmmr.minimize_app, ocmmr.maximize_app, ocmmr.restore_app, ocmmr.switch_btwn_apps, cbv.set_volume, cbv.set_brightness, crdf.create_folder, crdf.rename_folder, crdf.delete_folder, crdfile.create_add_content_file, crdfile.rename_file, crdfile.delete_file, cup.change_user_preferences]
tools_by_name = {tool.name: tool for tool in tools}
llmwithtools = llm.bind_tools(tools)

# NODE
system_msg = SystemMessage(content=
    "You are Neura_Command, an Agentic AI created by Abhinav Ranjan Jha. "
    "You can control the entire computer system through provided tools. "
    "USE internet_search to search the internet for recent information. "
    "USE web_scraper to know all about given link/url or extract/scrape information from it. All types of websites are supported "
    "If the user provides an invalid Windows application name that you don't know, treat it as valid and proceed. "
    "More tools will be added later. Use tools when needed.\n\n"
    "After using internet_search or web_scraper, list the final URLs under a 'Sources:' section at last "
    "for ex:\n"
    "Sources:\n"
    "1. www.example.com\n"
    "2. www.example2.com\n"
    "etc.\n"
    "Always respond in Markdown, stay accurate, logical, and agentic and always do what user says no excuses."
    f"User's name is {name}."
)

def call_llm_node(state: MessagesState):
    
    messages = state["messages"]
    if not any(msg.__class__.__name__ == "SystemMessage" for msg in messages):
        messages.insert(0, system_msg)
        
    response = llmwithtools.invoke(messages)
    return {"messages": [response]}

def execute_tool_calls_node(state: MessagesState):
    """
    Executes all tool calls from the last message dynamically.

    Args:
        state (MessagesState): The current state containing messages and tool calls.

    Returns:
        dict: A dictionary with 'messages' containing the outputs of all executed tools.
    """
    last_message = state["messages"][-1]
    tool_outputs = []


    # Map your tool names to the actual callable functions
    tools_map = {
        "internet_search": research_tools.internet_search,
        "web_scraper": research_tools.web_scraper,
        "close_app": ocmmr.close_app,
        "minimize_app": ocmmr.minimize_app,
        "maximize_app": ocmmr.maximize_app,
        "restore_app": ocmmr.restore_app,
        "open_app": ocmmr.open_app,
        "switch_btwn_apps": ocmmr.switch_btwn_apps,
        "set_volume": cbv.set_volume,
        "set_brightness": cbv.set_brightness,
        "create_folder": crdf.create_folder,
        "rename_folder": crdf.rename_folder,
        "delete_folder": crdf.delete_folder,
        "create_add_content_file": crdfile.create_add_content_file,
        "rename_file": crdfile.rename_file,
        "delete_file": crdfile.delete_file,
        "change_user_preferences": cup.change_user_preferences,
        
    }

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]

        if tool_name in tools_map:
            print(Fore.YELLOW + f"Invoking {tool_name} with args: {args}" + Style.RESET_ALL)
            try:
                result = tools_map[tool_name].invoke(args)
                tool_outputs.append(ToolMessage(tool_call_id=tool_call['id'], content=str(result)))
                if tool_name == "internet_search":
                    print(Fore.YELLOW + f"[Tool Executed] 'query': '{result['query']}', 'follow_up_questions': '{result['follow_up_questions']}', 'result': 'Too long can't show.....', 'response_time': {result['response_time']}" + Style.RESET_ALL + "\n")
                    
                elif tool_name == "web_scraper":
                    result_urls = [item['url'] for item in result['results'] if 'url' in item]

                    failed_urls = [item['url'] for item in result['failed_results'] if 'url' in item]
                    
                    print(Fore.YELLOW + f"[Tool Executed] 'results_url': '{result_urls}', 'failed_urls':'{failed_urls}', 'response_time': {result['response_time']}" + Style.RESET_ALL + "\n")
                else:
                    print(Fore.YELLOW + f"[Tool Executed] {result}" + Style.RESET_ALL + "\n")
            except Exception as e:
                tool_outputs.append(
                    ToolMessage(tool_call_id=tool_call['id'], content=f"Error executing {tool_name}: {e}")
                )
        else:
            print(f"No tool found with name '{tool_name}'")
            tool_outputs.append(
                ToolMessage(tool_call_id=tool_call['id'], content=f"No tool found with name '{tool_name}'")
            )

    return {"messages": tool_outputs}

def should_call_tools(state: MessagesState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    else:
        return "end"
    
# GRAPH
graph = StateGraph(MessagesState)
graph.add_node("llm_node", call_llm_node)
graph.add_node("execute_tool_calls_node", execute_tool_calls_node)

graph.add_edge(START,"llm_node")
graph.add_conditional_edges(
    "llm_node", 
    should_call_tools,
    {
        "tools": "execute_tool_calls_node",
        "end": END,
    }
)
graph.add_edge("execute_tool_calls_node", "llm_node")


checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "ARJ"}}

# RESULTS
solution = """
Do solution i) first if problem persists do ii) if still then do iii)
Try one of the following Solution:
    i) Wait for few seconds and message again
    ii) Restart the App
    iii) Change the model
"""

async def run_loop():
    os.system("cls" if os.name == "nt" else "clear")
    print("\nNeura_Command is ready. Type your query below.\n")
    console = Console()
    
    while True:
        user_input = input("\n" + Fore.CYAN + r"You: " + Style.RESET_ALL)
        print()

        input_data = {"messages": [HumanMessage(content=user_input)]}
        markdown_text = ""

        try:
            with Progress(
                SpinnerColumn("arc"),
                TextColumn("[progress.description]{task.description}"),
                transient=True   # hides after exit
            ) as progress:

                task = progress.add_task("Generating response...", start=False)

                running = True

                def update_description():
                    messages = [
                        "Analyzing your message...",
                        "Thinking deeply...",
                        "Generating response...",
                        "Almost done..."
                    ]
                    i = 0
                    while running:
                        progress.update(task, description=messages[i % len(messages)])
                        i += 1
                        time.sleep(0.9)

                updater_thread = threading.Thread(target=update_description)
                updater_thread.start()

                progress.start_task(task)
                result = app.invoke(input_data, config)

                running = False
                updater_thread.join()

            # Convert to Markdown
            markdown_text = result["messages"][-1].content
            md = Markdown(markdown_text)
            console.print(md, style="#2bbd65")

                 
        except exceptions.InvalidArgument as e:
            print(Fore.RED + "Invalid input:", e)

        except exceptions.PermissionDenied as e:
            print(Fore.RED + "Permission denied:", e)

        except exceptions.ResourceExhausted as e:
            print(Fore.RED + f"Rate limit exceeded:" + Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX + solution + Style.RESET_ALL)

        except exceptions.NotFound as e:
            print(Fore.RED + "Model not found:", e)

        except exceptions.InternalServerError as e:
            print(Fore.RED + "Server error:", e)

        except exceptions.ServiceUnavailable as e:
            print(Fore.RED + "Service unavailable:", e)

        except exceptions.BadRequest as e:
            print(Fore.RED + "Invalid Api Key Provided:", str(e))
            clear_gemini_api(ENV_PATH)
            
        except Exception as e:
            print(Fore.RED + "Unknown error:", e)
            clear_gemini_api(ENV_PATH)

            
asyncio.run(run_loop())