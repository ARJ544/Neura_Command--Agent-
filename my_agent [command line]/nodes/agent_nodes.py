from utils import change_user_preferences_tool as cup
from utils import research_tools
from utils import open_close_min_max_res_apps_tool as ocmmr
from utils import control_brightness_volume_tool as cbv
from utils import create_rename_delete_folder_tool as crdf
from utils import create_rename_delete_file_tool as crdfile
from utils import move_file_folder as mff
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
from colorama import Fore, Style, init
from config import llmwithtools, name

init(autoreset=True)

system_msg = SystemMessage(content=
    "You are Neura_Command, an Agentic AI created by Abhinav Ranjan Jha. "
    "Speak the language in which the user talks/want to talk. "
    "You can control the entire computer system through provided tools. Also you can do general talks. "
    "You can also solve any type of question. "
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
        "move_file_folder": mff.move_file_folder,
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
