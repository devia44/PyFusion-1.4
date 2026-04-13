# PyFusion Plugin Tutorial

## Plugin Structure

```
my_plugin/
├── manifest.json
└── main.py
```

---

## 1 manifest.json

```json
{
    "id": "my_plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "My awesome plugin",
    "author": "Your Name",
    "entry": "main.py",
    "class": "MyPlugin",
    "requires_license": false
}
```

---

## 2 main.py

```python
# -*- coding: utf-8 -*-
"""
My Plugin for PyFusion
"""

import tkinter as tk
from tkinter import ttk, messagebox


class MyPlugin:
    def __init__(self, app):
        self.app = app
        self.name = "My Plugin"
        self.version = "1.0.0"
    
    def get_menu_items(self):
        return [
            {"label": "My Plugin Window", "command": self.open_window},
            {"label": "My Plugin Info", "command": self.show_info}
        ]
    
    def open_window(self):
        window = tk.Toplevel(self.app.root)
        window.title(self.name)
        window.geometry("400x300")
        
        ttk.Label(window, text=self.name, font=('TkDefaultFont', 14, 'bold')).pack(pady=20)
        ttk.Label(window, text="Your content here").pack()
    
    def show_info(self):
        messagebox.showinfo("Info", f"{self.name} v{self.version}")
```

---

## 3 build.py (.pfp)

```python
import json
import zipfile
import os

# Read manifest
with open('manifest.json', 'r') as f:
    manifest = json.load(f)

# Files to include
files = ['manifest.json', 'main.py']

# Create .pfp file
output = f"{manifest['id']}-v{manifest['version']}.pfp"
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
    for file in files:
        if os.path.exists(file):
            zf.write(file)
            print(f"Added: {file}")

print(f"✅ Plugin built: {output}")
```

---

## 4 Installation

1. Run `build.py` → creates `.pfp` file
2. Open PyFusion → `Plugins` → `Plugin Installer`
3. Click `Install from File` → select `.pfp`
4. Done! Plugin appears in `Plugins` menu

---

## 5 Full Example: Hello World Plugin

### manifest.json
```json
{
    "id": "hello_world",
    "name": "Hello World",
    "version": "1.0.0",
    "description": "Says hello",
    "author": "PyFusion",
    "entry": "main.py",
    "class": "HelloWorld",
    "requires_license": false
}
```

### main.py
```python
import tkinter as tk
from tkinter import ttk, messagebox

class HelloWorld:
    def __init__(self, app):
        self.app = app
    
    def get_menu_items(self):
        return [{"label": "Say Hello", "command": self.say_hello}]
    
    def say_hello(self):
        messagebox.showinfo("Hello", "Hello from my plugin!")
```

### build.py
```python
import json, zipfile, os

with open('manifest.json') as f:
    manifest = json.load(f)

output = f"{manifest['id']}.pfp"
with zipfile.ZipFile(output, 'w') as zf:
    for file in ['manifest.json', 'main.py']:
        if os.path.exists(file):
            zf.write(file)

print(f"✅ {output}")
```

---

## API Methods

| Method | Description |
|--------|-------------|
| `self.app.root` | Main window |
| `self.app.current_editor` | Current editor |
| `self.app.set_status("text")` | Set status bar |
| `self.app.open_editor_tab()` | Open editor |
| `self.app.add_tab(title, widget)` | Add tab |

---

## Ready to use!
1. Create folder `my_plugin/`
2. Add `manifest.json` and `main.py`
3. Run `build.py`
4. Install `.pfp` in PyFusion
