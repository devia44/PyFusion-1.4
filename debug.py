# -*- coding: utf-8 -*-
"""
Debug system with rotation and console
"""

import sys
import io
import traceback
from datetime import datetime
from pathlib import Path
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

class Debugger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.log_path = Path(__file__).parent.parent / "debug.log"
        self.max_size = 1024 * 1024  # 1 MB
        self.console_window = None
        self.original_stderr = sys.stderr
        self.original_stdout = sys.stdout
        
        # Перехват stdout/stderr
        self.output_buffer = io.StringIO()
        sys.stderr = self
        sys.stdout = self
        
        self.log("=" * 60)
        self.log(f"PyFusion 1.4 Debug System Started")
        self.log(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log("=" * 60)
    
    def write(self, text):
        """Перехват вывода"""
        if text and text.strip():
            self.log(text.strip(), to_console=False)
        self.output_buffer.write(text)
    
    def flush(self):
        self.output_buffer.flush()
    
    def log(self, msg, to_console=True):
        """Запись в лог"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] {msg}"
        
        # Запись в файл
        try:
            # Проверка размера
            if self.log_path.exists() and self.log_path.stat().st_size > self.max_size:
                self.rotate_log()
            
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(formatted_msg + "\n")
        except:
            pass
        
        # Вывод в консоль разработчика
        if to_console and self.console_window and self.console_window.winfo_exists():
            self.console_window.add_text(formatted_msg + "\n")
    
    def rotate_log(self):
        """Ротация лога при превышении размера"""
        try:
            backup_path = self.log_path.with_suffix(".old.log")
            if self.log_path.exists():
                self.log_path.rename(backup_path)
            self.log("Log rotated (max size exceeded)", to_console=False)
        except:
            pass
    
    def log_error(self, error):
        """Логирование ошибки с traceback"""
        self.log(f"ERROR: {str(error)}")
        self.log(traceback.format_exc())
    
    def open_console(self, app):
        """Открыть консоль разработчика"""
        if self.console_window and self.console_window.winfo_exists():
            self.console_window.lift()
            return
        
        self.console_window = DevConsole(self, app)
    
    def close_console(self):
        if self.console_window and self.console_window.winfo_exists():
            self.console_window.destroy()
        self.console_window = None


class DevConsole(tk.Toplevel):
    def __init__(self, debugger, app):
        super().__init__()
        self.debugger = debugger
        self.app = app
        self.title("PyFusion Developer Console v1.4")
        self.geometry("900x500")
        self.configure(bg='#1e1e1e')
        
        try:
            icon_path = Path(__file__).parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except:
            pass
        
        self.setup_ui()
        self.check_errors()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Центрирование
        self.update_idletasks()
        x = app.root.winfo_x() + (app.root.winfo_width() - 900) // 2
        y = app.root.winfo_y() + (app.root.winfo_height() - 500) // 2
        self.geometry(f"+{x}+{y}")
    
    def setup_ui(self):
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Clear Console", command=self.clear).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Check Errors", command=self.check_errors).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Check Files", command=self.check_all_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Run GC", command=self.run_gc).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(toolbar, text="Level:").pack(side=tk.LEFT, padx=(20, 5))
        self.level_var = tk.StringVar(value="INFO")
        level_combo = ttk.Combobox(toolbar, textvariable=self.level_var, 
                                    values=["DEBUG", "INFO", "WARNING", "ERROR"], 
                                    state="readonly", width=8)
        level_combo.pack(side=tk.LEFT)
        
        # Main text area
        self.text_area = scrolledtext.ScrolledText(self, bg='#1e1e1e', fg='#d4d4d4',
                                                   font=("Consolas", 10), wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure tags
        self.text_area.tag_config("ERROR", foreground="#f44747")
        self.text_area.tag_config("WARNING", foreground="#ffcc00")
        self.text_area.tag_config("INFO", foreground="#4ec9b0")
        self.text_area.tag_config("DEBUG", foreground="#808080")
        
        # Status bar
        self.status_label = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def add_text(self, text, level="INFO"):
        """Добавить текст с подсветкой"""
        levels_order = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        current_level = levels_order.get(self.level_var.get(), 1)
        msg_level = levels_order.get(level, 1)
        
        if msg_level >= current_level:
            self.text_area.insert(tk.END, text, level)
            self.text_area.see(tk.END)
    
    def clear(self):
        self.text_area.delete(1.0, tk.END)
        self.debugger.log("Console cleared", to_console=False)
    
    def check_errors(self):
        """Проверка ошибок в логе"""
        self.add_text("\n" + "=" * 60 + "\n", "INFO")
        self.add_text("ERROR CHECK - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n", "INFO")
        self.add_text("=" * 60 + "\n", "INFO")
        
        try:
            log_path = Path(__file__).parent.parent / "debug.log"
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                errors = [l for l in lines if "ERROR" in l or "Traceback" in l or "Exception" in l]
                
                if errors:
                    self.add_text(f"\nFound {len(errors)} errors/issues:\n\n", "WARNING")
                    for err in errors[-20:]:  # последние 20
                        self.add_text(err, "ERROR")
                else:
                    self.add_text("\nNo errors found!\n", "INFO")
            else:
                self.add_text("\nNo log file found\n", "WARNING")
        except Exception as e:
            self.add_text(f"\nError reading log: {e}\n", "ERROR")
    
    def check_all_files(self):
        """Проверка всех файлов на ошибки"""
        self.add_text("\n" + "=" * 60 + "\n", "INFO")
        self.add_text("FILE CHECK - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n", "INFO")
        self.add_text("=" * 60 + "\n", "INFO")
        
        pyfusion_root = Path(__file__).parent.parent
        errors_found = []
        
        # Проверка Python файлов
        for py_file in pyfusion_root.rglob("*.py"):
            if "debug.log" not in str(py_file) and "__pycache__" not in str(py_file):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Простая проверка синтаксиса
                        compile(content, str(py_file), 'exec')
                except SyntaxError as e:
                    errors_found.append(f"SYNTAX ERROR in {py_file}: {e}")
                except Exception as e:
                    errors_found.append(f"ERROR in {py_file}: {e}")
        
        # Проверка наличия критических папок
        required_dirs = ["core", "utils", "files/pics", "plugins"]
        for d in required_dirs:
            if not (pyfusion_root / d).exists():
                errors_found.append(f"MISSING FOLDER: {d}")
        
        if errors_found:
            self.add_text(f"\nFound {len(errors_found)} issues:\n\n", "WARNING")
            for err in errors_found:
                self.add_text(f"  • {err}\n", "ERROR")
        else:
            self.add_text("\nAll files OK!\n", "INFO")
        
        self.status_label.config(text=f"Checked {len(list(pyfusion_root.rglob('*.py')))} files")
    
    def run_gc(self):
        """Запуск сборщика мусора"""
        import gc
        self.add_text("\n" + "=" * 60 + "\n", "INFO")
        self.add_text("GARBAGE COLLECTOR\n", "INFO")
        self.add_text("=" * 60 + "\n", "INFO")
        
        before = len(gc.get_objects())
        collected = gc.collect()
        after = len(gc.get_objects())
        
        self.add_text(f"Objects before: {before}\n", "DEBUG")
        self.add_text(f"Objects collected: {collected}\n", "INFO")
        self.add_text(f"Objects after: {after}\n", "DEBUG")
        self.add_text(f"Memory freed: {collected * 8} bytes approx\n", "INFO")
    
    def on_close(self):
        self.debugger.console_window = None
        self.destroy()


# Глобальный экземпляр
_debugger = None

def get_debugger():
    global _debugger
    if _debugger is None:
        _debugger = Debugger()
    return _debugger
