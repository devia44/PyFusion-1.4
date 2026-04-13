# -*- coding: utf-8 -*-
"""
Настройки приложения
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

try:
    import ttkbootstrap as tb
    TTKBOOTSTRAP = True
except ImportError:
    TTKBOOTSTRAP = False


class Settings:
    def __init__(self, app):
        self.app = app
        self.dialog = None
        
    def _set_icon(self, window):
        """Установка иконки"""
        try:
            icon_path = Path(__file__).parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                window.iconbitmap(str(icon_path))
        except:
            pass
        
    def show_dialog(self):
        """Показать диалог настроек"""
        if TTKBOOTSTRAP:
            self.dialog = tb.Toplevel(self.app.root)
        else:
            self.dialog = tk.Toplevel(self.app.root)
            self.dialog.configure(bg='#2b2b2b')
            
        self._set_icon(self.dialog)
        self.dialog.title(self.app.i18n.get("settings.title"))
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        self.dialog.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - 500) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - 400) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        self.dialog.transient(self.app.root)
        self.dialog.grab_set()
        
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text=self.app.i18n.get("settings.general"))
        self.create_general_settings(general_frame)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text=self.app.i18n.get("settings.save"),
                  command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.app.i18n.get("settings.cancel"),
                  command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        self.dialog.wait_window()
        return True
        
    def create_general_settings(self, parent):
        """Создание общих настроек"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        lang_frame = ttk.Frame(frame)
        lang_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(lang_frame, text=self.app.i18n.get("settings.language") + ":",
                 width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        self.lang_var = tk.StringVar(value=self.app.i18n.current_language)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                  values=["en", "ru"], state="readonly", width=10)
        lang_combo.pack(side=tk.LEFT)
        
        theme_frame = ttk.Frame(frame)
        theme_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(theme_frame, text=self.app.i18n.get("settings.theme") + ":",
                 width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        themes = ["darkly", "superhero", "cyborg", "vapor", "solar", "flatly", "journal"]
        self.theme_var = tk.StringVar(value=self.app.config.get("theme", "darkly"))
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                   values=themes, state="readonly", width=15)
        theme_combo.pack(side=tk.LEFT)
        
    def save_settings(self):
        """Сохранение настроек"""
        new_lang = self.lang_var.get()
        if new_lang != self.app.i18n.current_language:
            self.app.i18n.set_language(new_lang)
            self.app.config.set("language", new_lang)
            self.app.update_ui_texts()
        
        new_theme = self.theme_var.get()
        if new_theme != self.app.config.get("theme"):
            self.app.config.set("theme", new_theme)
            messagebox.showinfo("Info", "Theme will be applied after restart")
        
        self.dialog.destroy()
