# -*- coding: utf-8 -*-
"""
Менеджер плагинов PyFusion
"""

import os
import sys
import json
import zipfile
import shutil
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading
import urllib.request
import tempfile


def log_debug(msg):
    try:
        log_path = Path(__file__).parent.parent / "debug.log"
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"[PluginManager] {msg}\n")
    except:
        pass


class PluginManager:
    def __init__(self, app):
        self.app = app
        self.plugins = {}
        self.plugins_dir = Path(__file__).parent.parent / "plugins"
        self.load_plugins()
    
    def load_plugins(self):
        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir(exist_ok=True)
            log_debug(f"Created plugins directory: {self.plugins_dir}")
            return
        
        log_debug(f"Loading plugins from: {self.plugins_dir}")
        
        for plugin_folder in self.plugins_dir.iterdir():
            if plugin_folder.is_dir() and not plugin_folder.name.startswith('_'):
                manifest = plugin_folder / "manifest.json"
                if manifest.exists():
                    self.load_plugin(plugin_folder, manifest)
    
    def load_plugin(self, plugin_folder, manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            plugin_id = manifest.get("id")
            plugin_name = manifest.get("name")
            plugin_version = manifest.get("version")
            plugin_entry = manifest.get("entry", "main.py")
            plugin_class = manifest.get("class", "Plugin")
            
            log_debug(f"Loading plugin: {plugin_name} v{plugin_version}")
            
            if manifest.get("requires_license", False):
                license_file = plugin_folder / ".license"
                if not license_file.exists():
                    log_debug(f"Plugin {plugin_name} requires license, not loading")
                    return
                else:
                    log_debug(f"License found for {plugin_name}")
            
            entry_file = plugin_folder / plugin_entry
            if entry_file.exists():
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{plugin_id}", 
                    str(entry_file)
                )
                if spec is None:
                    log_debug(f"Failed to create spec for {entry_file}")
                    return
                    
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"plugins.{plugin_id}"] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, plugin_class):
                    plugin_instance = getattr(module, plugin_class)(self.app)
                    self.plugins[plugin_id] = {
                        "instance": plugin_instance,
                        "manifest": manifest,
                        "folder": plugin_folder,
                        "enabled": True
                    }
                    log_debug(f"Plugin loaded: {plugin_name} v{plugin_version}")
                    
                    if hasattr(plugin_instance, 'on_enable'):
                        plugin_instance.on_enable()
                else:
                    log_debug(f"Class {plugin_class} not found in {plugin_id}")
            else:
                log_debug(f"Entry file not found: {entry_file}")
                
        except Exception as e:
            log_debug(f"Error loading plugin {plugin_folder}: {e}")
            import traceback
            log_debug(traceback.format_exc())
    
    def get_plugin(self, plugin_id):
        return self.plugins.get(plugin_id, {}).get("instance")
    
    def get_all_plugins(self):
        return self.plugins
    
    def install_plugin(self, plugin_path):
        try:
            log_debug(f"Installing plugin from: {plugin_path}")
            
            with zipfile.ZipFile(plugin_path, 'r') as zf:
                manifest_data = None
                for file in zf.namelist():
                    if file.endswith('manifest.json'):
                        manifest_data = json.loads(zf.read(file))
                        break
                
                if not manifest_data:
                    return False, "manifest.json not found"
                
                plugin_id = manifest_data.get("id")
                if not plugin_id:
                    return False, "Plugin ID not specified"
                
                plugin_folder = self.plugins_dir / plugin_id
                if plugin_folder.exists():
                    shutil.rmtree(plugin_folder)
                
                plugin_folder.mkdir(exist_ok=True)
                zf.extractall(plugin_folder)
                
                manifest_path = plugin_folder / "manifest.json"
                if manifest_path.exists():
                    self.load_plugin(plugin_folder, manifest_path)
                
                return True, f"Plugin {manifest_data.get('name')} installed"
                
        except Exception as e:
            log_debug(f"Install error: {e}")
            return False, str(e)
    
    def uninstall_plugin(self, plugin_id):
        try:
            plugin_folder = self.plugins_dir / plugin_id
            if plugin_folder.exists():
                if plugin_id in self.plugins:
                    plugin = self.plugins[plugin_id]["instance"]
                    if hasattr(plugin, 'on_disable'):
                        plugin.on_disable()
                    del self.plugins[plugin_id]
                
                shutil.rmtree(plugin_folder)
                log_debug(f"Plugin uninstalled: {plugin_id}")
                return True
        except Exception as e:
            log_debug(f"Uninstall error: {e}")
        return False
    
    def get_plugin_menu_items(self):
        items = []
        for plugin_id, plugin_data in self.plugins.items():
            plugin = plugin_data["instance"]
            if hasattr(plugin, 'get_menu_items'):
                try:
                    plugin_items = plugin.get_menu_items()
                    for item in plugin_items:
                        item['plugin_id'] = plugin_id
                        items.append(item)
                except Exception as e:
                    log_debug(f"Error getting menu items from {plugin_id}: {e}")
        return items


class PluginInstaller:
    def __init__(self, app):
        self.app = app
    
    def open_installer(self):
        window = tk.Toplevel(self.app.root)
        window.title("Plugin Installer")
        window.geometry("700x550")
        window.configure(bg='#2b2b2b')
        
        try:
            icon_path = Path(__file__).parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                window.iconbitmap(str(icon_path))
        except:
            pass
        
        title_frame = ttk.Frame(window)
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(title_frame, text="Plugin Installer", 
                 font=('TkDefaultFont', 18, 'bold')).pack(side=tk.LEFT)
        
        list_frame = ttk.LabelFrame(window, text=" Installed Plugins ", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("name", "version", "author", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        self.tree.heading("name", text="Plugin")
        self.tree.heading("version", text="Version")
        self.tree.heading("author", text="Author")
        self.tree.heading("status", text="Status")
        self.tree.column("name", width=200)
        self.tree.column("version", width=80)
        self.tree.column("author", width=150)
        self.tree.column("status", width=80)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        
        detail_frame = ttk.LabelFrame(window, text=" Plugin Details ", padding=10)
        detail_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.detail_text = tk.Text(detail_frame, height=4, bg='#1e1e1e', fg='#d4d4d4',
                                   font=("Consolas", 9), wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(window)
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Button(btn_frame, text="Install from File", 
                  command=self.install_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Install from URL", 
                  command=self.install_from_url).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Uninstall", 
                  command=self.uninstall_plugin).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", 
                  command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", 
                  command=window.destroy).pack(side=tk.RIGHT, padx=5)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.refresh_list()
        
        window.update_idletasks()
        x = self.app.root.winfo_x() + (self.app.root.winfo_width() - 700) // 2
        y = self.app.root.winfo_y() + (self.app.root.winfo_height() - 550) // 2
        window.geometry(f"+{x}+{y}")
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for plugin_id, plugin_data in self.app.plugin_manager.plugins.items():
            manifest = plugin_data["manifest"]
            enabled = plugin_data["enabled"]
            
            self.tree.insert("", tk.END, values=(
                manifest.get("name", plugin_id),
                manifest.get("version", "1.0"),
                manifest.get("author", "Unknown"),
                "Enabled" if enabled else "Disabled"
            ), tags=(plugin_id,))
    
    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        plugin_name = item['values'][0]
        
        for plugin_id, plugin_data in self.app.plugin_manager.plugins.items():
            if plugin_data["manifest"].get("name") == plugin_name:
                manifest = plugin_data["manifest"]
                details = f"ID: {plugin_id}\n"
                details += f"Name: {manifest.get('name', 'N/A')}\n"
                details += f"Version: {manifest.get('version', 'N/A')}\n"
                details += f"Author: {manifest.get('author', 'N/A')}\n"
                details += f"Description: {manifest.get('description', 'N/A')}"
                
                self.detail_text.delete(1.0, tk.END)
                self.detail_text.insert(1.0, details)
                break
    
    def install_from_file(self):
        file = filedialog.askopenfilename(
            title="Select Plugin",
            filetypes=[("PyFusion Plugin", "*.pfp"), ("ZIP files", "*.zip")]
        )
        if file:
            success, msg = self.app.plugin_manager.install_plugin(file)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_list()
            else:
                messagebox.showerror("Error", msg)
    
    def install_from_url(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Install from URL")
        dialog.geometry("450x150")
        dialog.configure(bg='#2b2b2b')
        
        ttk.Label(dialog, text="Enter Plugin URL:", 
                 font=('TkDefaultFont', 11)).pack(pady=15)
        
        url_entry = ttk.Entry(dialog, width=50)
        url_entry.pack(pady=5, padx=20)
        
        def do_install():
            url = url_entry.get().strip()
            if url:
                try:
                    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
                        urllib.request.urlretrieve(url, tmp.name)
                        success, msg = self.app.plugin_manager.install_plugin(tmp.name)
                        os.unlink(tmp.name)
                        
                        if success:
                            messagebox.showinfo("Success", msg)
                            self.refresh_list()
                            dialog.destroy()
                        else:
                            messagebox.showerror("Error", msg)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Install", command=do_install).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        dialog.transient(self.app.root)
        dialog.grab_set()
        url_entry.focus()
    
    def uninstall_plugin(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a plugin to uninstall")
            return
        
        item = self.tree.item(selection[0])
        plugin_name = item['values'][0]
        
        for plugin_id, plugin_data in self.app.plugin_manager.plugins.items():
            if plugin_data["manifest"].get("name") == plugin_name:
                if messagebox.askyesno("Confirm", f"Uninstall {plugin_name}?"):
                    self.app.plugin_manager.uninstall_plugin(plugin_id)
                    self.refresh_list()
                    self.detail_text.delete(1.0, tk.END)
                break
