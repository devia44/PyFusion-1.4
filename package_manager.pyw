# -*- coding: utf-8 -*-
"""
Package Manager (PyPI only)
"""

import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class PackageManager(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI"""
        # Title
        title = ttk.Label(self, text="PyPI Package Manager",
                         font=('TkDefaultFont', 14, 'bold'))
        title.pack(pady=15)
        
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Install package
        install_frame = ttk.LabelFrame(container, text="Install Package")
        install_frame.pack(fill=tk.X, pady=10)
        
        inner = ttk.Frame(install_frame)
        inner.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(inner, text="Package name:").pack(side=tk.LEFT)
        self.package_name = ttk.Entry(inner, width=30)
        self.package_name.pack(side=tk.LEFT, padx=10)
        ttk.Button(inner, text="Install",
                  command=self.install_package, style="success.TButton").pack(side=tk.LEFT)
        
        # Uninstall package
        uninstall_frame = ttk.LabelFrame(container, text="Uninstall Package")
        uninstall_frame.pack(fill=tk.X, pady=10)
        
        inner2 = ttk.Frame(uninstall_frame)
        inner2.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(inner2, text="Package name:").pack(side=tk.LEFT)
        self.uninstall_name = ttk.Entry(inner2, width=30)
        self.uninstall_name.pack(side=tk.LEFT, padx=10)
        ttk.Button(inner2, text="Uninstall",
                  command=self.uninstall_package, style="danger.TButton").pack(side=tk.LEFT)
        
        # Installed packages list
        list_frame = ttk.LabelFrame(container, text="Installed Packages")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Button(list_frame, text="Refresh List",
                  command=self.list_packages).pack(pady=5)
        
        self.package_list = tk.Listbox(list_frame, bg='#1e1e1e', fg='#d4d4d4',
                                       height=10)
        self.package_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output
        output_frame = ttk.LabelFrame(container, text="Output")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output_text = ScrolledText(output_frame, height=8, bg='#1e1e1e',
                                        fg='#d4d4d4', font=("Consolas", 9))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Kit info
        kit_frame = ttk.Frame(container)
        kit_frame.pack(pady=10)
        
        ttk.Label(kit_frame,
                 text="PyFusion Kit adds:",
                 font=('TkDefaultFont', 9, 'bold'),
                 foreground='#4ec9b0').pack()
        
        ttk.Label(kit_frame,
                 text="• Install from GitHub",
                 font=('TkDefaultFont', 9),
                 foreground='#808080').pack()
        ttk.Label(kit_frame,
                 text="• PyInstaller Pro for EXE builds",
                 font=('TkDefaultFont', 9),
                 foreground='#808080').pack()
    
    def run_pip_command(self, cmd, success_msg=None):
        """Run pip command"""
        def run():
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"> {' '.join(cmd)}\n\n")
            
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                
                stdout, _ = process.communicate(timeout=60)
                self.output_text.insert(tk.END, stdout)
                
                if process.returncode == 0 and success_msg:
                    self.after(0, lambda: messagebox.showinfo("Success", success_msg))
                    self.after(100, self.list_packages)
                    
            except subprocess.TimeoutExpired:
                self.output_text.insert(tk.END, "\n[ERROR] Timeout exceeded\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"\n[ERROR] {str(e)}\n")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def install_package(self):
        """Install package"""
        package = self.package_name.get().strip()
        if not package:
            messagebox.showerror("Error", "Enter package name")
            return
        
        self.run_pip_command(
            [sys.executable, "-m", "pip", "install", package],
            f"Package {package} installed"
        )
    
    def uninstall_package(self):
        """Uninstall package"""
        package = self.uninstall_name.get().strip()
        if not package:
            messagebox.showerror("Error", "Enter package name")
            return
        
        if messagebox.askyesno("Confirm", f"Uninstall package {package}?"):
            self.run_pip_command(
                [sys.executable, "-m", "pip", "uninstall", "-y", package],
                f"Package {package} uninstalled"
            )
    
    def list_packages(self):
        """List installed packages"""
        def run():
            self.package_list.delete(0, tk.END)
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "list"],
                    capture_output=True, text=True, timeout=30
                )
                for line in result.stdout.split('\n')[2:]:
                    if line.strip():
                        self.after(0, lambda l=line: self.package_list.insert(tk.END, l.strip()))
            except Exception as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def update_texts(self):
        pass
