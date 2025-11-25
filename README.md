```python
my_agent [command line]/                          # 📁 Root Project Directory (Executable entry lives here)
│
├─ utils/                          # 🔧 All low-level system tools (core actions)
│    ├─ __init__.py                # Package initializer
│    ├─ change_user_preferences_tool.py            # Tool: update user name / API keys
│    ├─ open_close_min_max_res_apps_tool.py        # Tool: open/close/min/max/restore/switch apps
│    ├─ control_brightness_volume_tool.py          # Tool: set brightness & volume
│    ├─ create_rename_delete_folder_tool.py        # Tool: folder operations (create/rename/delete)
│    ├─ create_rename_delete_file_tool.py          # Tool: file operations (create/rename/delete)
│    └─ research_tools.py                          # Tool: internet_search + web_scraper
│
├─ nodes/                          # 🧠 LangGraph node logic (LLM + tool execution flow)
│    ├─ __init__.py                # Package initializer
│    └─ agent_nodes.py             # Contains call_llm_node, execute_tool_calls_node, should_call_tools
│
├─ core/                           # ⚙️ Runtime engine: prompt loop, LangGraph execution
│    ├─ __init__.py                # Package initializer
│    └─ runner.py                  # Async terminal UI + LangGraph graph builder + message loop
│
├─ config.py                       # 🛠️ Environment setup, LLM initialization, tool binding, system prompt
│
└─ main.py                         # 🚀 Application entry point (used to build .exe)
```