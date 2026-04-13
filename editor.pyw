# -*- coding: utf-8 -*-
"""
Редактор кода с подсветкой синтаксиса
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

try:
    import ttkbootstrap as tb
    TTKBOOTSTRAP = True
except ImportError:
    TTKBOOTSTRAP = False


class CodeEditor(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.parent = parent
        self.current_file = None
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text=self.app.i18n.get("editor.new"),
                  command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=self.app.i18n.get("editor.open"),
                  command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=self.app.i18n.get("editor.save"),
                  command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=self.app.i18n.get("editor.run"),
                  command=self.run_code).pack(side=tk.LEFT, padx=2)
        
        # Editor
        self.text = ScrolledText(self, wrap=tk.WORD, undo=True,
                                 font=("Consolas", 11),
                                 bg='#1e1e1e', fg='#d4d4d4',
                                 insertbackground='white',
                                 selectbackground='#264f78')
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.setup_syntax_highlighting()
        
        # Bind hotkeys
        self.text.bind('<Control-s>', lambda e: self.save_file())
        self.text.bind('<Control-o>', lambda e: self.open_file())
        self.text.bind('<Control-n>', lambda e: self.new_file())
        self.text.bind('<Control-r>', lambda e: self.run_code())
        self.text.bind('<KeyRelease>', self.on_key_release)
        
    def setup_syntax_highlighting(self):
        """Настройка подсветки синтаксиса"""
        self.text.tag_configure("keyword", foreground="#569CD6")
        self.text.tag_configure("string", foreground="#CE9178")
        self.text.tag_configure("comment", foreground="#6A9955")
        self.text.tag_configure("function", foreground="#DCDCAA")
        self.text.tag_configure("number", foreground="#B5CEA8")
        self.text.tag_configure("error", foreground="#f44747")
        
    def highlight_syntax(self, event=None):
        """Подсветка синтаксиса"""
        keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif',
                   'for', 'while', 'return', 'try', 'except', 'finally',
                   'with', 'as', 'lambda', 'yield', 'async', 'await',
                   'and', 'or', 'not', 'in', 'is', 'None', 'True', 'False']
        
        for tag in ["keyword", "string", "comment", "function", "number"]:
            self.text.tag_remove(tag, 1.0, tk.END)
        
        for keyword in keywords:
            start = 1.0
            while True:
                pos = self.text.search(r'\m' + keyword + r'\M', start, tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.text.tag_add("keyword", pos, end)
                start = end
        
    def on_key_release(self, event):
        """Обработка нажатия клавиш"""
        self.highlight_syntax()
        if hasattr(self.app, 'set_status'):
            if self.current_file:
                self.app.set_status(f"{self.app.i18n.get('editor.opened')}: {os.path.basename(self.current_file)}")
            else:
                self.app.set_status(self.app.i18n.get("editor.new_file"))
        
    def new_file(self):
        """Создание нового файла"""
        self.text.delete(1.0, tk.END)
        self.current_file = None
        if hasattr(self.app, 'set_status'):
            self.app.set_status(self.app.i18n.get("editor.new_file"))
        if isinstance(self.parent, (tk.Toplevel,)) or (TTKBOOTSTRAP and isinstance(self.parent, tb.Window)):
            self.parent.title("New File - Editor")
        
    def open_file(self):
        """Открытие файла"""
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, content)
                self.current_file = file_path
                self.highlight_syntax()
                
                if hasattr(self.app, 'config'):
                    self.app.config.add_recent_file(file_path)
                    
                if hasattr(self.app, 'set_status'):
                    self.app.set_status(f"{self.app.i18n.get('editor.opened')}: {os.path.basename(file_path)}")
                    
                if isinstance(self.parent, (tk.Toplevel,)) or (TTKBOOTSTRAP and isinstance(self.parent, tb.Window)):
                    self.parent.title(f"{os.path.basename(file_path)} - Editor")
                    
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
    def save_file(self):
        """Сохранение файла"""
        if self.current_file:
            try:
                content = self.text.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                if hasattr(self.app, 'set_status'):
                    self.app.set_status(f"{self.app.i18n.get('editor.saved')}: {os.path.basename(self.current_file)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.save_as()
            
    def save_as(self):
        """Сохранить как"""
        file_path = filedialog.asksaveasfilename(defaultextension=".py")
        if file_path:
            self.current_file = file_path
            self.save_file()
            if isinstance(self.parent, (tk.Toplevel,)) or (TTKBOOTSTRAP and isinstance(self.parent, tb.Window)):
                self.parent.title(f"{os.path.basename(file_path)} - Editor")
                
    def run_code(self):
        """Запуск кода"""
        if not self.current_file:
            messagebox.showwarning("Warning", self.app.i18n.get("editor.save_first"))
            return
            
        self.save_file()
        
        # Создаем окно вывода
        if TTKBOOTSTRAP:
            output_window = tb.Toplevel(self)
        else:
            output_window = tk.Toplevel(self)
            
        output_window.title(self.app.i18n.get("editor.output"))
        output_window.geometry("700x500")
        output_window.configure(bg='#1e1e1e')
        
        # Установка иконки
        try:
            icon_path = Path(__file__).parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                output_window.iconbitmap(str(icon_path))
        except:
            pass
        
        # Output text area
        output_frame = ttk.Frame(output_window)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        output_text = ScrolledText(output_frame, bg='#1e1e1e', fg='#d4d4d4',
                                   font=("Consolas", 10))
        output_text.pack(fill=tk.BOTH, expand=True)
        
        output_text.tag_config("error", foreground="#f44747")
        output_text.tag_config("success", foreground="#4ec9b0")
        
        # Кнопка закрытия
        btn_frame = ttk.Frame(output_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(btn_frame, text="Close", command=output_window.destroy).pack(side=tk.RIGHT)
        
        # Центрируем окно
        output_window.update_idletasks()
        x = self.winfo_toplevel().winfo_x() + (self.winfo_toplevel().winfo_width() - 700) // 2
        y = self.winfo_toplevel().winfo_y() + (self.winfo_toplevel().winfo_height() - 500) // 2
        output_window.geometry(f"+{x}+{y}")
        
        # Запуск кода
        try:
            process = subprocess.Popen(
                [sys.executable, self.current_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(self.current_file)
            )
            
            stdout, stderr = process.communicate(timeout=30)
            
            if stdout:
                output_text.insert(tk.END, stdout)
            if stderr:
                output_text.insert(tk.END, stderr, "error")
                
            if process.returncode == 0:
                output_text.insert(tk.END, f"\n[Process finished with exit code 0]\n", "success")
            else:
                output_text.insert(tk.END, f"\n[Process finished with exit code {process.returncode}]\n", "error")
            
            if hasattr(self.app, 'set_status'):
                self.app.set_status(f"Code executed (exit code: {process.returncode})")
                
        except subprocess.TimeoutExpired:
            process.kill()
            output_text.insert(tk.END, f"\n{self.app.i18n.get('editor.timeout')}\n", "error")
            if hasattr(self.app, 'set_status'):
                self.app.set_status("Execution timeout")
        except Exception as e:
            output_text.insert(tk.END, f"\n[Error] {str(e)}\n", "error")
            if hasattr(self.app, 'set_status'):
                self.app.set_status(f"Error: {str(e)[:50]}")
                  
    def update_texts(self):
        """Обновление текстов при смене языка"""
        pass
