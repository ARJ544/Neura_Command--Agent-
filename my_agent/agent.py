from utils import open_close_min_max_res_apps_tool as ocmmr
from utils import research_tools
from langgraph.graph import StateGraph, MessagesState, START, END
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage,SystemMessage, ToolMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
import asyncio

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

    
# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    
)
tools = [research_tools.internet_search, research_tools.web_scraper, ocmmr.open_app, ocmmr.close_app, ocmmr.minimize_app, ocmmr.maximize_app, ocmmr.restore_app]
tools_by_name = {tool.name: tool for tool in tools}
llmwithtools = llm.bind_tools(tools)

# NODE
system_msg = SystemMessage(content=
    "You are Neura_Command, an Agentic AI created by Abhinav Ranjan Jha. "
    "You can control the entire computer system through provided tools. "
    "Currently available tools: [internet_search, web_scraper, open_app, close_app, minimize_app, maximize_app, restore_app] "
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
        # Add more tools here as needed
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

# input1 = {"messages": [HumanMessage(content="open control panel")]}
# RESULTS — Continuous loop mode (REPL)

async def run_loop():
    print("\nNeura_Command is ready. Type your query below.\n")

    while True:
        user_input = input("\nYou: ")
        
        input_data = {"messages": [HumanMessage(content=user_input)]}

        async for event in app.astream_events(input_data, config):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    print(chunk, end="", flush=True)

        print()  # new line after response


asyncio.run(run_loop())