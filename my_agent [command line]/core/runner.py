import warnings
warnings.filterwarnings(
    "ignore", 
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater."
)

from langgraph.graph import StateGraph, MessagesState, START, END
from google.api_core import exceptions
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style as PTStyle
from colorama import Fore, Style, init
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import os, asyncio
from nodes.agent_nodes import call_llm_node, execute_tool_calls_node, should_call_tools
from config import ENV_PATH

init(autoreset=True)

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
default_msg = f"""
{Fore.CYAN + Style.BRIGHT}I can help you manage and automate a wide range of tasks on your system, including:{Style.RESET_ALL}

 {Fore.YELLOW}• Web Search:{Fore.WHITE} Quickly look up information from across the internet.
 {Fore.YELLOW}• Web Scraping:{Fore.WHITE} Extract structured data from specific websites.
 {Fore.YELLOW}• Application Control:{Fore.WHITE} Open, close, minimize, maximize, restore, and switch between apps.
 {Fore.YELLOW}• System Volume Control:{Fore.WHITE} Increase, decrease, or mute your system volume.
 {Fore.YELLOW}• System Brightness Control:{Fore.WHITE} Adjust your device's brightness levels.
 {Fore.YELLOW}• File & Folder Management:{Fore.WHITE} Create, rename, Move or delete files and directories.
 {Fore.YELLOW}• User Preference Management:{Fore.WHITE} Update your personal preferences such as Name, Gemini_API_Key, or Tavily_API_Key.

{Fore.CYAN}To update your name or API keys, simply tell the Agent to modify your user preferences.{Style.RESET_ALL}

{Fore.MAGENTA}Shortcuts:{Style.RESET_ALL}
 {Fore.GREEN}• (Enter){Fore.WHITE} → New Line
 {Fore.GREEN}• (Ctrl + C){Fore.WHITE} → Exit the application
 {Fore.GREEN}• (Ctrl + D){Fore.WHITE} → Submit Query
"""

async def run_loop():
    os.system("cls" if os.name == "nt" else "clear")
    print("\033c", end="")
    print(default_msg)
    
    console = Console()
    kb = KeyBindings()
    
    @kb.add(Keys.Enter)
    def _(event):
        event.current_buffer.insert_text('\n')
    
    @kb.add(Keys.ControlD)
    def _(event):
        event.current_buffer.validate_and_handle()
    session = PromptSession(multiline=True, key_bindings=kb,)
    
    style = PTStyle.from_dict({
    'prompt': 'ansicyan bold',})


    while True:
        try:
            # user_input = await session.prompt_async("\n" + [('class:prompt', r"You: ")], style=style)
            user_input = await session.prompt_async(
                [('', '\n'), ('class:prompt', 'You: ')],
                style=style
            )

            if not user_input.strip():
                continue

            print()

            input_data = {"messages": [HumanMessage(content=user_input)]}

            with Progress(
                SpinnerColumn("arc"),
                TextColumn("[progress.description]{task.description}"),
                transient=True
            ) as progress:
                progress.add_task("Generating response...", start=True)
                result = await app.ainvoke(input_data, config)

            markdown_text = result["messages"][-1].content
            console.print(Markdown(markdown_text), style="#2bbd65")

        except KeyboardInterrupt:
            print("\nExiting.... Wait...")
            break

        except asyncio.CancelledError:
            print("\nExiting.... Wait...")
            break
        
        except EOFError:
            print("\nExiting.... Wait...")
            break
        
        except exceptions.InternalServerError as e:
            print(Fore.RED + "Internal Server Error:", e)
        
        except exceptions.TooManyRequests as e:
            print(Fore.RED + "Too many Requests Change Gemini Model: ", e)
            print(Fore.MAGENTA + solution + Style.RESET_ALL)
                   
        except exceptions.BadRequest as e:
            print(Fore.RED + "Bad Request:", e)
            if "api key not valid" in str(e).lower():
                clear_gemini_api(ENV_PATH)
            print(Fore.MAGENTA + solution + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + "Unknown error:", e)
            if "api key not valid" in str(e).lower():
                clear_gemini_api(ENV_PATH)
            print(Fore.MAGENTA + solution + Style.RESET_ALL)
