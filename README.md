# 📘 PyFusion Documentation

**Version 1.4** | *A modular development toolkit for Python developers*

---

## 📋 Table of Contents

1. [What is PyFusion?](#what-is-pyfusion)
2. [Current State](#current-state)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Core Features](#core-features)
6. [Plugin System](#plugin-system)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Building from Source](#building-from-source)
11. [License](#license)

---

## 🧰 What is PyFusion?

PyFusion is a **modular development environment** built with Python and Tkinter.

Think of it as a **Swiss Army knife for developers** — a collection of tools packed into one application, with a plugin system that lets you add whatever you need.

### Core Philosophy

- **Modular** — Use only what you need
- **Extensible** — Write your own plugins
- **Lightweight** — No heavy dependencies
- **Transparent** — Open source, no hidden magic

---

## 📍 Current State

**Version: 1.4** (stable)

PyFusion is a **one-person project**. I built it because I needed a tool that does a bit of everything without installing 10 different programs.

### What works right now:

| Feature | Status |
|---------|--------|
| Code Editor (Python) | ✅ Stable |
| File Creator | ✅ Stable |
| PNG to ICO Converter | ✅ Stable |
| Set Folder Icon (Windows) | ✅ Stable |
| PyPI Package Manager | ✅ Stable |
| Plugin System | ✅ Stable |
| Tabbed Interface | ✅ Stable |
| Dark Theme | ✅ Stable |

### What's coming (PyFusion Kit):

- Git Manager (clone, commit, push, pull)
- Archiver (ZIP, TAR.GZ, TAR.BZ2)
- Advanced Icon Tools (batch convert, icon editor)
- PyInstaller Pro (build standalone EXEs)
- Code Templates (Flask, FastAPI, React, Vue, Docker)

**Why not yet?** Because I'm working alone and I want each feature to be solid before releasing it.

---

## 💻 Installation

### Option 1: Run from source (recommended for developers)

```bash
git clone https://github.com/devia44/PyFusion-1.4.git
cd PyFusion
python run.pyw
```

### Option 2: Standalone EXE

> ⚠️ Not yet available. Coming after PyFusion Kit is ready.

### Requirements

- Python 3.7 or higher (32-bit or 64-bit)
- Windows (Linux/macOS may work but not fully tested)

### Optional dependencies (for full functionality)

```bash
pip install pillow      # For icon conversion
pip install gitpython   # For Git features (Kit only)
pip install ttkbootstrap # For additional themes
```

Without these, PyFusion falls back to built-in alternatives.

---

## 🎮 Quick Start

### First Launch

1. Run `python app.pyw`
2. You'll see the **Welcome Tab** with:
   - Quick action buttons
   - Keyboard shortcuts list
   - Kit status (if installed)

### Your First File

1. Click **New File** or press `Ctrl+N`
2. Type some Python code
3. Press `Ctrl+S` to save
4. Press `Ctrl+R` to run it

### Install a Package

1. Go to `View → Package Manager`
2. Type `requests` (or any package name)
3. Click **Install**

### Create a Plugin

1. Create folder `plugins/my_plugin/`
2. Add `manifest.json` and `main.py` (see [Plugin System](#plugin-system))
3. Restart PyFusion
4. Find your plugin in `Plugins` menu

---

## 🛠️ Core Features

### 1. Code Editor

**Open:** `View → Editor` or click "Open Editor" on Welcome tab

**Features:**
- Run Python code (`Ctrl+R`) with output in separate window
- Open/Save files (`Ctrl+O`, `Ctrl+S`)
- Undo/Redo (`Ctrl+Z`, `Ctrl+Y`)
- Cut/Copy/Paste (`Ctrl+X`, `Ctrl+C`, `Ctrl+V`)

**Run Output Window:**
- Shows stdout (normal output in white)
- Shows stderr (errors in red)
- Shows exit code
- Timeout after 30 seconds

### 2. File Creator

**Open:** `View → File Creator`

Create any file with custom content:

| Field | Description |
|-------|-------------|
| Filename | Name of the file (without extension) |
| Extension | Choose from 15+ common extensions |
| Content | Your file content (supports multiline) |

Click **Create** — file appears in current directory.

### 3. Icon Tools

**Open:** `View → Icon Tools`

**Convert PNG to ICO:**
1. Click Browse and select a PNG file
2. Check the icon sizes you want (16, 32, 48, 64, 128, 256 px)
3. Click **Convert to ICO**
4. Choose where to save the `.ico` file

**Set Folder Icon (Windows only):**
1. Browse for a folder
2. Browse for an `.ico` file
3. Click **Apply Icon to Folder**

> Note: This modifies `desktop.ini` and sets folder attributes. Works on Windows only.

### 4. Package Manager

**Open:** `View → Package Manager`

**Install:**
- Type package name → Click Install

**Uninstall:**
- Type package name → Click Uninstall → Confirm

**List installed:**
- Click **Refresh List**

Uses `pip` internally. Shows real-time output.

---

## 🔌 Plugin System

### What Plugins Can Do

- Add items to the `Plugins` menu
- Open custom windows
- Add new tabs to the notebook
- Access PyFusion's core functions
- Save/load data

### Plugin Structure

```
plugins/
└── your_plugin/
    ├── manifest.json    # Required
    └── main.py          # Required
```

### manifest.json (minimum)

```json
{
    "id": "your_plugin",
    "name": "Your Plugin",
    "version": "1.0.0",
    "entry": "main.py",
    "class": "YourPlugin"
}
```

### main.py (minimum)

```python
class YourPlugin:
    def __init__(self, app):
        self.app = app
    
    def get_menu_items(self):
        return [
            {"label": "My Action", "command": self.do_something}
        ]
    
    def do_something(self):
        print("Plugin works!")
```

### Plugin API

| Access | What you get |
|--------|--------------|
| `self.app.root` | Main Tkinter window |
| `self.app.current_editor` | Current editor instance (if open) |
| `self.app.notebook` | Tab container (ttk.Notebook) |
| `self.app.add_tab(title, widget)` | Add a new tab |
| `self.app.set_status(text)` | Change status bar text |
| `self.app.open_editor_tab()` | Open/code editor tab |
| `self.app.config.get(key)` | Get config value |
| `self.app.config.set(key, value)` | Set config value |

### Installing Plugins

1. Copy plugin folder to `PyFusion/plugins/`
2. Restart PyFusion
3. Plugin appears in `Plugins` menu

### Building .pfp (Plugin Package)

```python
# build.py
import zipfile, os

files = ['manifest.json', 'main.py']
with zipfile.ZipFile('my_plugin.pfp', 'w') as zf:
    for f in files:
        if os.path.exists(f):
            zf.write(f)
```

Run: `python build.py`

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New File |
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save File |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+W` | Close Current Tab |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+X` | Cut |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+,` | Settings |
| `Ctrl+R` | Run Code (in Editor) |

---

## ⚙️ Configuration

### Config File Location

```
C:\Users\[YourName]\.pyfusion\config.json
```

### Default Settings

```json
{
    "language": "en",
    "theme": "darkly",
    "editor_font": "Consolas",
    "editor_font_size": 11,
    "auto_save": true,
    "recent_files": [],
    "max_recent_files": 10
}
```

### Changing Settings

1. `Tools → Settings` (or `Ctrl+,`)
2. Change language or theme
3. Click **Save**
4. Restart for theme changes

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **PIL not found** | `pip install pillow` |
| **GitPython not found** | `pip install gitpython` (for Kit) |
| **ttkbootstrap not found** | `pip install ttkbootstrap` (fallback works) |
| **Kit not loading** | Check `.license` file exists |
| **Plugin not showing** | Check `manifest.json` syntax and folder structure |

### Debug Log

PyFusion creates `debug.log` in the root folder:

```
[2026-01-01 12:00:00] PyFusion 1.4 Starting...
[2026-01-01 12:00:01] Kit available: False
[2026-01-01 12:00:02] Plugin loaded: My Plugin
```

### Developer Console

Open via: `PyFusion 1.4 → Developer Console`

**Features:**
- View live logs
- Check for errors in log file
- Scan all `.py` files for syntax errors
- Run garbage collector
---

## 💬 One More Thing

I built this alone, in my free time, because I wanted a tool that works the way I think.

**You can help by:**
- Writing plugins
- Reporting bugs
- Suggesting features
- Sharing the project

**You can also:**
- Fork it
- Remix it
- Break it
- Fix it
- Make it your own

That's what open source is about.

— **PyFusion Team of One** 🧑‍💻

---

## 🔗 Links

- **Source code:** [GitHub](https://github.com/yourusername/PyFusion)
- **Report issues:** [Issues](https://github.com/yourusername/PyFusion/issues)
- **Plugin examples:** `/plugins/examples/`

---

**Built with 🐍 Python | Version 1.4 | 2026**

