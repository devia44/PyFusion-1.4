# -*- coding: utf-8 -*-
"""
Управление отдельными окнами
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

try:
    import ttkbootstrap as tb
    TTKBOOTSTRAP = True
except ImportError:
    TTKBOOTSTRAP = False


class WindowManager:
    def __init__(self, app):
        self.app = app
        self.windows = []
        
    def _set_icon(self, window):
        """Установка иконки для окна"""
        try:
            icon_path = Path(__file__).parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                window.iconbitmap(str(icon_path))
        except:
            pass
        
    def create_window(self, window_type="editor"):
        """Создание нового окна"""
        if TTKBOOTSTRAP:
            window = tb.Toplevel(self.app.root)
        else:
            window = tk.Toplevel(self.app.root)
            window.configure(bg='#2b2b2b')
        
        self._set_icon(window)
        
        if window_type == "editor":
            from core.editor import CodeEditor
            content = CodeEditor(window, self.app)
            content.pack(fill=tk.BOTH, expand=True)
            window.title(f"Editor - {len([w for w in self.windows if w.winfo_exists()]) + 1}")
            
        elif window_type == "file_creator":
            from core.file_creator import FileCreator
            content = FileCreator(window, self.app)
            content.pack(fill=tk.BOTH, expand=True)
            window.title(self.app.i18n.get("window.file_creator"))
            
        elif window_type == "icon_tools":
            from core.icon_tools import IconTools
            content = IconTools(window, self.app)
            content.pack(fill=tk.BOTH, expand=True)
            window.title(self.app.i18n.get("window.icon_tools"))
            
        elif window_type == "package_manager":
            from core.package_manager import PackageManager
            content = PackageManager(window, self.app)
            content.pack(fill=tk.BOTH, expand=True)
            window.title(self.app.i18n.get("window.package_manager"))
            
        window.geometry("800x600")
        window.minsize(600, 400)
        
        window.update_idletasks()
        main_x = self.app.root.winfo_x()
        main_y = self.app.root.winfo_y()
        offset = len(self.windows) * 30
        window.geometry(f"+{main_x + 50 + offset}+{main_y + 50 + offset}")
        
        self.windows.append(window)
        
        window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(window))
        
        return window
        
    def close_window(self, window):
        """Закрытие окна"""
        if window in self.windows:
            self.windows.remove(window)
        window.destroy()
        
    def close_all_windows(self):
        """Закрытие всех окон"""
        for window in self.windows[:]:
            if window.winfo_exists():
                window.destroy()
        self.windows.clear()
        
    def tile_windows(self):
        """Размещение окон плиткой"""
        windows = [self.app.root] + [w for w in self.windows if w.winfo_exists()]
        if len(windows) <= 1:
            return
            
        screen_width = self.app.root.winfo_screenwidth()
        screen_height = self.app.root.winfo_screenheight() - 50
        
        n = len(windows)
        cols = int(n ** 0.5)
        rows = (n + cols - 1) // cols
        
        width = screen_width // cols
        height = screen_height // rows
        
        for i, window in enumerate(windows):
            col = i % cols
            row = i // cols
            x = col * width
            y = row * height
            window.geometry(f"{width}x{height}+{x}+{y}")
            
    def cascade_windows(self):
        """Размещение окон каскадом"""
        windows = [w for w in self.windows if w.winfo_exists()]
        if not windows:
            return
            
        main_x = self.app.root.winfo_x()
        main_y = self.app.root.winfo_y()
        
        offset = 30
        x, y = main_x + 50, main_y + 50
        
        for window in windows:
            window.geometry(f"800x600+{x}+{y}")
            x += offset
            y += offset
