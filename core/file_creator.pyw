# -*- coding: utf-8 -*-
"""
Инструмент создания файлов
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox


class FileCreator(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        # Title
        title = ttk.Label(self, text=self.app.i18n.get("creator.title"),
                         font=('TkDefaultFont', 14, 'bold'))
        title.pack(pady=15)
        
        # Main container
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Filename
        name_frame = ttk.Frame(container)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text=self.app.i18n.get("creator.filename") + ":",
                 width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.filename = ttk.Entry(name_frame)
        self.filename.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Extension
        ext_frame = ttk.Frame(container)
        ext_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ext_frame, text=self.app.i18n.get("creator.extension") + ":",
                 width=12, anchor=tk.W).pack(side=tk.LEFT)
        
        extensions = ['txt', 'py', 'pyw', 'java', 'cpp', 'c', 'html', 'css', 
                     'js', 'json', 'xml', 'yaml', 'md', 'csv', 'sql', 'sh', 'bat']
        self.ext = ttk.Combobox(ext_frame, values=extensions, state="readonly")
        self.ext.set('txt')
        self.ext.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Content
        ttk.Label(container, text=self.app.i18n.get("creator.content") + ":",
                 anchor=tk.W).pack(fill=tk.X, pady=(15, 5))
        
        self.content = tk.Text(container, height=15, bg='#1e1e1e', fg='#d4d4d4',
                              insertbackground='white', font=("Consolas", 10))
        self.content.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text=self.app.i18n.get("creator.create"),
                  command=self.create_file, style="success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.app.i18n.get("creator.clear"),
                  command=self.clear).pack(side=tk.LEFT, padx=5)
                  
    def create_file(self):
        """Создание файла"""
        name = self.filename.get().strip()
        ext = self.ext.get()
        content = self.content.get(1.0, tk.END).strip()
        
        if not name:
            messagebox.showerror("Error", self.app.i18n.get("creator.error_no_name"))
            return
            
        filename = f"{name}.{ext}"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo(self.app.i18n.get("creator.success"),
                              f"{self.app.i18n.get('creator.created')}: {filename}")
            if hasattr(self.app, 'set_status'):
                self.app.set_status(f"Created: {filename}")
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def clear(self):
        """Очистка полей"""
        self.filename.delete(0, tk.END)
        self.content.delete(1.0, tk.END)
        
    def update_texts(self):
        """Обновление текстов при смене языка"""
        pass
