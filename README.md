# 🔧 PyFusion

**PyFusion** is a universal "Swiss Army knife" for software developers. A powerful environment with plugins, code editor, and a set of tools for everyday tasks.

---

## ✨ Features

| Category | Tools |
|----------|-------|
| **Code Editor** | Syntax highlighting, Python execution, hotkeys |
| **Plugins** | Full .pfp plugin system, Plugin Installer |
| **Git** | Clone, commit, push, pull, branches (via PyFusion Kit) |
| **Archiver** | ZIP, TAR.GZ, TAR.BZ2 – create and extract |
| **Icons** | PNG to ICO converter, set folder icons |
| **Package Manager** | PyPI install/uninstall/list |
| **Templates** | Ready-to-use code templates for various languages |
| **PyInstaller Pro** | Build standalone .exe files with options |

---

## 🧩 Plugin System

PyFusion has a built-in plugin system. Plugins use `.pfp` extension and can add:
- Menu items
- Custom windows
- New tools and features

**Plugin example:**
```json
{
    "id": "my_plugin",
    "name": "My Plugin",
    "entry": "main.py",
    "class": "MyPlugin"
}
```

---

## 🔌 Creating Plugins

1. Create `manifest.json` and `main.py`
2. Run `build.py` to create `.pfp` file
3. Install via Plugin Installer

**Minimal plugin:**
```python
class MyPlugin:
    def __init__(self, app):
        self.app = app
    
    def get_menu_items(self):
        return [{"label": "Hello", "command": self.say_hello}]
    
    def say_hello(self):
        print("Hello from plugin!")
```
---

## 📦 PyFusion Kit (Extended)

The Kit adds advanced features:
- Full Git integration (clone, commit, push, pull, branches)
- Archiver (ZIP, TAR.GZ, TAR.BZ2)
- Advanced icon tools (batch convert, file type icons)
- PyInstaller Pro (build executables)
- Code templates

---

## 🚀 Quick Start

1. **Download** PyFusion.exe or run from source
2. **Write code** in the built-in editor
3. **Install plugins** via `Plugins → Plugin Installer`
4. **Use tools** from the menu or hotkeys

---

## ⌨️ Hotkeys

| Key | Action |
|-----|--------|
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save |
| `Ctrl+W` | Close tab |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+X/C/V` | Cut/Copy/Paste |
| `Ctrl+,` | Settings |


---

## 📄 License

MIT License – free and open source

---

## 👥 Authors

PyFusion Team (or just @devia44)
