# -*- coding: utf-8 -*-
"""
My Plugin for PyFusion
Author: Your Name
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path


class MyPlugin:
    """Main plugin class"""
    
    def __init__(self, app):
        self.app = app
        self.name = "My Plugin"
        self.version = "1.0.0"
        
    def on_enable(self):
        """Called when plugin is enabled"""
        print(f"[{self.name}] Plugin enabled")
        
    def on_disable(self):
        """Called when plugin is disabled"""
        print(f"[{self.name}] Plugin disabled")
        
    def get_menu_items(self):
        """Return menu items for this plugin"""
        return [
            {
                "label": "My Plugin",
                "command": self.open_main_window
            },
            {
                "label": "My Plugin Settings",
                "command": self.open_settings
            }
        ]
        
    def get_toolbar_items(self):
        """Return toolbar buttons for this plugin"""
        return [
            {
                "label": "My Plugin",
                "command": self.open_main_window,
                "icon": None  # Optional: path to icon
            }
        ]
        
    def open_main_window(self):
        """Open the main plugin window"""
        window = tk.Toplevel(self.app.root)
        window.title(f"{self.name} v{self.version}")
        window.geometry("600x500")
        window.configure(bg='#2b2b2b')
        
        # Set window icon
        self._set_window_icon(window)
        
        # Main content
        main_frame = ttk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text=self.name,
                         font=('TkDefaultFont', 16, 'bold'))
        title.pack(pady=10)
        
        # Description
        desc = ttk.Label(main_frame, text="Your plugin description here",
                        wraplength=500)
        desc.pack(pady=5)
        
        # Content area
        content = ttk.LabelFrame(main_frame, text=" Plugin Content ", padding=10)
        content.pack(fill=tk.BOTH, expand=True, pady=20)
        
        ttk.Label(content, text="Add your widgets here").pack(pady=20)
        
        # Status bar
        status = ttk.Label(window, text="Ready", relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Center window
        window.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - 600) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - 500) // 2
        window.geometry(f"+{x}+{y}")
        
    def open_settings(self):
        """Open settings window"""
        window = tk.Toplevel(self.app.root)
        window.title(f"{self.name} Settings")
        window.geometry("400x300")
        window.configure(bg='#2b2b2b')
        
        self._set_window_icon(window)
        
        main_frame = ttk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Plugin Settings",
                 font=('TkDefaultFont', 14, 'bold')).pack(pady=10)
        
        # Example setting
        setting_frame = ttk.Frame(main_frame)
        setting_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(setting_frame, text="Setting 1:").pack(side=tk.LEFT)
        ttk.Entry(setting_frame).pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        ttk.Button(main_frame, text="Save", command=window.destroy).pack(pady=20)
        
        window.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - 400) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - 300) // 2
        window.geometry(f"+{x}+{y}")
        
    def _set_window_icon(self, window):
        """Set window icon"""
        try:
            icon_path = Path(__file__).parent.parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                window.iconbitmap(str(icon_path))
        except:
            pass
