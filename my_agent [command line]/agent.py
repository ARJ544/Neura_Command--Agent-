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
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core import exceptions
from langchain_core.messages import HumanMessage,SystemMessage, ToolMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
import asyncio
load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    env_path = ".env"

    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            values = f.readlines()

        if values == [] or len(values) < 3:
            name = input("Enter your name: ")
            gemini_key = input("Enter your Gemini API: ")
            tavily_key = input("Enter your Tavily API: ")

            with open(env_path, 'w') as f:
                f.write(f"NAME={name}\n")
                f.write(f"GOOGLE_API_KEY={gemini_key}\n")
                f.write(f"TAVILY_API_KEY={tavily_key}\n")

            values = [f"NAME={name}\n", f"GOOGLE_API_KEY={gemini_key}\n", f"TAVILY_API_KEY={tavily_key}\n"]

        name = values[0].strip().split("=")[1]
        gemini_key = values[1].strip().split("=")[1]
        tavily_key = values[2].strip().split("=")[1]

        print(f"name={name}, gemini_key={gemini_key}, tavily_key={tavily_key}")

    else:
        name = input("Enter your name: ")
        gemini_key = input("Enter your Gemini API: ")
        tavily_key = input("Enter your Tavily API: ")

        with open(env_path, 'w') as f:
            f.write(f"NAME={name}\n")
            f.write(f"GOOGLE_API_KEY={gemini_key}\n")
            f.write(f"TAVILY_API_KEY={tavily_key}\n")

        print("New .env file created successfully!")
else:
    gemini_key = os.getenv("GOOGLE_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    name = os.environ.get("NAME")

if not gemini_key or not tavily_key or not name:
    with open(env_path, 'r') as f:
            values = f.readlines()

            if values == [] or len(values) < 3:
                name = input("Enter your name: ")
                gemini_key = input("Enter your Gemini API: ")
                tavily_key = input("Enter your Tavily API: ")

                with open(env_path, 'w') as f:
                    f.write(f"NAME={name}\n")
                    f.write(f"GOOGLE_API_KEY={gemini_key}\n")
                    f.write(f"TAVILY_API_KEY={tavily_key}\n")

                values = [f"NAME={name}\n", f"GOOGLE_API_KEY={gemini_key}\n", f"TAVILY_API_KEY={tavily_key}\n"]

            name = values[0].strip().split("=")[1]
            gemini_key = values[1].strip().split("=")[1]
            tavily_key = values[2].strip().split("=")[1]

            print(f"name={name}, gemini_key={gemini_key}, tavily_key={tavily_key}")


# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
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
        
    print("\n" + "-----"*10 + " All Messages content " + "-----"*10)
    for msg in messages:
        if isinstance(msg, SystemMessage):
            print("system msg =", msg.content)
        elif isinstance(msg, HumanMessage):
            print("human msg =", msg.content)
        # elif isinstance(msg, ToolMessage):
        #     print(f"tool msg = {msg.content}")
        elif isinstance(msg, AIMessage):
            print("assistant msg =", msg.content)
            print("usage_metadata = ", msg.usage_metadata)
    print("-----"*10 + "End of All Messages content " + "-----"*10 + "\n")

    # print("-----"*50)
    # print(f"\nAll Messages = {"messages"}\n")
    print("-----"*10 + " Last Message content " + "-----"*10)
    print(f"\nLast message = {messages[-1]}\n")
    print("-----"*10 + "End of Last Message content " + "-----"*10)
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

    print("\n" + "-----" * 10 + " Tool Calls to be executed " + "-----" * 10)

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
            print(f"Invoking {tool_name} with args:", args)
            try:
                result = tools_map[tool_name].invoke(args)
                tool_outputs.append(ToolMessage(tool_call_id=tool_call['id'], content=str(result)))
            except Exception as e:
                tool_outputs.append(
                    ToolMessage(tool_call_id=tool_call['id'], content=f"Error executing {tool_name}: {e}")
                )
        else:
            print(f"No tool found with name '{tool_name}'")
            tool_outputs.append(
                ToolMessage(tool_call_id=tool_call['id'], content=f"No tool found with name '{tool_name}'")
            )

    print("-----" * 10 + " End of Tool Calls execution " + "-----" * 10 + "\n")

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
Try one of the following Solution:
    i) Wait for a minute
    ii) Restart the App
    iii) Change the model
"""

async def run_loop():
    os.system("cls" if os.name == "nt" else "clear")
    print("\nNeura_Command is ready. Type your query below.\n")

    while True:
        user_input = input(r"You: ")
        input_data = {"messages": [HumanMessage(content=user_input)]}
        
        try:
            async for event in app.astream_events(input_data, config):
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"]["chunk"].content
                    if chunk:
                        print(chunk, end="", flush=True)
                # print()
                        
        except exceptions.InvalidArgument as e:
            print("Invalid input:", e)

        except exceptions.PermissionDenied as e:
            print("Permission denied:", e)

        except exceptions.ResourceExhausted as e:
            print("Rate limit exceeded:", e)
            print(solution)

        except exceptions.NotFound as e:
            print("Model not found:", e)

        except exceptions.InternalServerError as e:
            print("Server error:", e)

        except exceptions.ServiceUnavailable as e:
            print("Service unavailable:", e)

        except Exception as e:
            print("Unknown error:", e)



asyncio.run(run_loop())