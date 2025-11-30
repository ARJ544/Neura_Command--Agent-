# 🔧 Tools Required (Complete Breakdown)

## 1. System Control

### 1.1 Detect active window
- pygetwindow
- psutil

### 1.2 Switch windows & applications
- pygetwindow
- pyautogui
- keyboard

### 1.3 Open/close/minimize/maximize apps
- subprocess
- pygetwindow
- pyautogui

### 1.4 Launch apps (name/path)
- subprocess
- os
- pathlib

### 1.5 Control system settings (brightness, volume)
- Windows: pycaw, screen_brightness_control 
- Linux: dbus, subprocess  
- Mac: osascript

---

## 2. File & Folder Operations

### 2.1 Create/rename/delete files
- os
- pathlib

### 2.2 Create/rename/delete folders
- os
- pathlib

### 2.3 Move/copy files & folders
- shutil
- pathlib

### 2.4 Extract ZIP/RAR
- shutil


### 2.6 Read txt, md, etc...
- python-docx
- Built-in file I/O
- pypandoc (for MD)

---

## 3. Web Automation

### 3.1 Open URL
- webbrowser
- selenium
- playwright

### 3.2 Click links/buttons
- selenium
- playwright
- pyautogui

---

## 4. Screen Understanding

### 4.1 OCR (screen text extract)
- pytesseract
- Pillow
- Tesseract OCR Engine (external)

### 4.2 Extract region (x1,y1 → x2,y2)
- Pillow
- pyautogui

### 4.3 Detect UI elements
- opencv-python
- pyautogui

### 4.4 Detect buttons/icons by image
- opencv-python
- pyautogui

### 4.5 Identify pop-ups & errors
- opencv-python
- pyautogui

---

## 5. Terminal Control

### 5.1 Execute commands
- subprocess
- os

### 5.2 Install packages
- subprocess

### 5.3 Git operations
- GitPython
- subprocess

### 5.4 Run scripts/commands
- subprocess
- os

### 5.5 Kill processes
- psutil

### 5.6 Monitor CPU/RAM
- psutil

---

## 6. Application-Specific Workflows

### Browser – Open/close/switch tabs
- selenium
- playwright
- pyautogui

---

## 7. Safety & Permissions

### 7.1 Ask confirmation
- tkinter (popup UI)

### 7.2 Maintain logs
- logging
- datetime

### 7.3 Allow/deny rule system
- json

### 7.4 Safe-mode execution
- Internal logic & exception handling

---

## 8. Developer Tools Integration

### 8.1 Auto-generate boilerplate code
- jinja2

### 8.2 Debugging assistance
- pdb
- logging

### 8.3 Auto-fix compile errors
- ast
- autopep8
- pylint

### 8.4 Run tests & interpret results
- pytest
- unittest

### 8.5 Suggest optimizations
- ast
- Code analyzers
