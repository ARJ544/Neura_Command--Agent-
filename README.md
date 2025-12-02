```python
📁 my_agent [command line]                  # 🚀 Root Project Directory (CLI entry lives here)
│
├─ core/                                       # ⚙️ Runtime Engine (execution + event loop)
│   ├─ __init__.py                             # Package initializer
│   └─ runner.py                               # Async runner, LangGraph builder, message loop
│
├─ nodes/                                      # 🧠 All LangGraph Node Logic
│   ├─ __init__.py                             # Package initializer
│   └─ agent_nodes.py                          # LLM call node, tool execution node, routing logic
│
├─ utils/                                      # 🔧 System Tools (OS actions + automation tools)
│   ├─ __init__.py                             # Package initializer
│   ├─ change_user_preferences_tool.py         # Tool: update username / preferences / API keys
│   ├─ control_brightness_volume_tool.py       # Tool: manage system brightness & volume
│   ├─ create_or_extract_zip_tool.py           # Tool: create zip, extract zip archives
│   ├─ create_rename_delete_file_tool.py       # Tool: create / rename / delete files
│   ├─ create_rename_delete_folder_tool.py     # Tool: create / rename / delete folders
│   ├─ move_file_folder.py                     # Tool: move files or directories
│   ├─ open_close_min_max_res_apps_tool.py     # Tool: open, close, min, max, restore apps
│   ├─ open_url_query_in_browser_tool.py       # Tool: open URLs or search queries in browser
│   ├─ read_file_tool.py                       # Tool: read file content (text, structured data)
│   ├─ read_screen_text_tool.py                # Tool: OCR / extract on-screen text
│   ├─ research_tools.py                       # Tool: internet search + lightweight web scraper
│   └─ terminal_control_tool.py                # Tool: run terminal commands (safe execution)
│
├─ config.py                                   # 🛠️ Config loader, LLM setup, tool binding,
│
└─ main.py                                     # 🏁 Application entry point (build .exe from here)
```