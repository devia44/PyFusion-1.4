# -*- coding: utf-8 -*-
"""
Plugin Creator - Создание плагинов
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import zipfile
from pathlib import Path


class PluginCreator:
    def __init__(self, app):
        self.app = app
    
    def get_menu_items(self):
        return [{
            "label": "Plugin Creator",
            "command": self.open_creator
        }]
    
    def open_creator(self):
        window = tk.Toplevel(self.app.root)
        window.title("Plugin Creator")
        window.geometry("700x650")
        window.configure(bg='#2b2b2b')
        
        try:
            icon_path = Path(__file__).parent.parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                window.iconbitmap(str(icon_path))
        except:
            pass
        
        # ВЕРХНЯЯ ПАНЕЛЬ С КНОПКАМИ
        top_frame = ttk.Frame(window)
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(top_frame, text="Plugin Creator", 
                 font=('TkDefaultFont', 14, 'bold')).pack(side=tk.LEFT)
        
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        def save_plugin():
            plugin_id = entries["id"].get().strip()
            plugin_name = entries["name"].get().strip()
            
            if not plugin_id or not plugin_name:
                messagebox.showerror("Error", "Plugin ID and Name are required")
                return
            
            manifest = {
                "id": plugin_id,
                "name": plugin_name,
                "version": entries["version"].get(),
                "description": entries["description"].get(),
                "author": entries["author"].get(),
                "entry": "main.py",
                "class": entries["class_name"].get(),
                "requires_license": self.license_var.get()
            }
            
            output = filedialog.asksaveasfilename(
                title="Save Plugin",
                defaultextension=".pfp",
                filetypes=[("PyFusion Plugin", "*.pfp")]
            )
            
            if output:
                try:
                    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
                        zf.writestr('manifest.json', json.dumps(manifest, indent=2))
                        zf.writestr('main.py', code_text.get(1.0, tk.END))
                        zf.writestr('__init__.py', f'from .main import {manifest["class"]}\n')
                    
                    messagebox.showinfo("Success", f"Plugin saved to:\n{output}")
                    window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        ttk.Button(btn_frame, text="Save Plugin", command=save_plugin).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Разделитель
        ttk.Separator(window).pack(fill=tk.X, padx=20, pady=5)
        
        # Форма
        form = ttk.LabelFrame(window, text=" Plugin Information ", padding=10)
        form.pack(fill=tk.X, padx=20, pady=10)
        
        fields = [
            ("Plugin ID:", "id", "my_plugin"),
            ("Plugin Name:", "name", "My Plugin"),
            ("Version:", "version", "1.0.0"),
            ("Description:", "description", "My awesome plugin"),
            ("Author:", "author", "Your Name"),
            ("Class Name:", "class_name", "MyPlugin"),
        ]
        
        entries = {}
        for label, key, default in fields:
            row = ttk.Frame(form)
            row.pack(fill=tk.X, pady=3)
            
            ttk.Label(row, text=label, width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(row, width=50)
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            entries[key] = entry
        
        options_frame = ttk.Frame(form)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.license_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Requires License", 
                       variable=self.license_var).pack(side=tk.LEFT, padx=5)
        
        # Редактор кода
        code_frame = ttk.LabelFrame(window, text=" Plugin Code (main.py) ", padding=10)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_frame = ttk.Frame(code_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        code_text = tk.Text(text_frame, wrap=tk.WORD, bg='#1e1e1e', fg='#d4d4d4',
                           font=("Consolas", 10), insertbackground='white')
        
        v_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=code_text.yview)
        code_text.configure(yscrollcommand=v_scroll.set)
        
        code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        template = '''# -*- coding: utf-8 -*-
"""
{description}
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path


class {class_name}:
    def __init__(self, app):
        self.app = app
        self.name = "{name}"
        self.version = "{version}"
    
    def get_menu_items(self):
        return [{{
            "label": self.name,
            "command": self.open_window
        }}]
    
    def open_window(self):
        window = tk.Toplevel(self.app.root)
        window.title(f"{{self.name}} v{{self.version}}")
        window.geometry("500x400")
        window.configure(bg='#2b2b2b')
        
        ttk.Label(window, text=self.name,
                 font=('TkDefaultFont', 14, 'bold')).pack(pady=20)
        ttk.Label(window, text="Your plugin content here").pack()
'''
        
        def update_template(*args):
            code_text.delete(1.0, tk.END)
            code_text.insert(1.0, template.format(
                name=entries["name"].get(),
                version=entries["version"].get(),
                description=entries["description"].get(),
                class_name=entries["class_name"].get()
            ))
        
        for entry in entries.values():
            entry.bind('<KeyRelease>', update_template)
        
        update_template()
        
        # НИЖНЯЯ ПАНЕЛЬ С КНОПКАМИ (для удобства)
        bottom_frame = ttk.Frame(window)
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(bottom_frame, text="Save Plugin", command=save_plugin).pack(side=tk.RIGHT, padx=5)
        ttk.Button(bottom_frame, text="Cancel", command=window.destroy).pack(side=tk.RIGHT, padx=5)
        
        window.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - 700) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - 650) // 2
        window.geometry(f"+{x}+{y}")

