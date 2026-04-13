# -*- coding: utf-8 -*-
"""
Главное приложение PyFusion
Version: 1.4
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import importlib.util
import traceback

# Инициализация дебаггера
from utils.debug import get_debugger
debug = get_debugger()

def log_debug(msg):
    debug.log(msg)

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

log_debug("=" * 60)
log_debug("PyFusion 1.4 Starting...")
log_debug("=" * 60)

# Проверка Kit
plugins_dir = Path(__file__).parent.parent / "plugins"
kit_plugin_path = plugins_dir / "pyfusion_kit"
kit_license = kit_plugin_path / ".license"

KIT_AVAILABLE = kit_license.exists()
log_debug(f"Kit available: {KIT_AVAILABLE}")

PyFusionKit = None

if KIT_AVAILABLE:
    init_files = list(kit_plugin_path.glob("__init__.*"))
    if init_files:
        init_file = init_files[0]
        try:
            spec = importlib.util.spec_from_file_location("pyfusion_kit", str(init_file))
            if spec:
                pyfusion_kit = importlib.util.module_from_spec(spec)
                sys.modules["pyfusion_kit"] = pyfusion_kit
                spec.loader.exec_module(pyfusion_kit)
                if hasattr(pyfusion_kit, 'PyFusionKit'):
                    PyFusionKit = pyfusion_kit.PyFusionKit
        except Exception as e:
            log_debug(f"Kit load error: {e}")
            KIT_AVAILABLE = False

try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
    TTKBOOTSTRAP_AVAILABLE = True
except ImportError:
    TTKBOOTSTRAP_AVAILABLE = False

from core.windows import WindowManager
from core.editor import CodeEditor
from core.file_creator import FileCreator
from core.icon_tools import IconTools
from core.settings import Settings
from core.package_manager import PackageManager
from core.plugin_manager import PluginManager, PluginInstaller
from utils.i18n import I18n
from utils.config import Config


class PyFusionApp:
    def __init__(self):
        try:
            self.config = Config()
            self.i18n = I18n()
            self.i18n.set_language(self.config.get("language", "en"))
            
            if TTKBOOTSTRAP_AVAILABLE:
                self.root = tb.Window(themename=self.config.get("theme", "darkly"))
            else:
                self.root = tk.Tk()
                self.setup_fallback_theme()
            
            self.window_manager = WindowManager(self)
            self.settings = Settings(self)
            self.kit = None
            
            if KIT_AVAILABLE and PyFusionKit:
                try:
                    self.kit = PyFusionKit(self)
                except Exception as e:
                    log_debug(f"Kit init error: {e}")
                    self.kit = None
            
            try:
                self.plugin_manager = PluginManager(self)
                self.plugin_installer = PluginInstaller(self)
            except Exception as e:
                log_debug(f"Plugin manager error: {e}")
                self.plugin_manager = None
                self.plugin_installer = None
            
            self.current_editor = None
            self.logo_img = None
            self.big_logo = None
            self.tab_frames = {}
            
            self.setup_window()
            self.create_menu()
            self.create_ui()
            self.bind_hotkeys()
            
        except Exception as e:
            log_debug(f"App init error: {e}\n{traceback.format_exc()}")
            raise
    
    def setup_fallback_theme(self):
        self.root.configure(bg='#1e1e1e')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='#d4d4d4')
        style.configure('TButton', background='#3c3c3c', foreground='#d4d4d4')
        style.configure('TEntry', fieldbackground='#2d2d2d', foreground='#d4d4d4')
        style.configure('TNotebook', background='#1e1e1e')
        style.configure('TNotebook.Tab', background='#3c3c3c', foreground='#d4d4d4', padding=[10, 2])
        style.map('TNotebook.Tab', background=[('selected', '#007acc')])
        
    def setup_window(self):
        title = "PyFusion 1.4"
        if KIT_AVAILABLE:
            title += " + Kit"
        self.root.title(f"{title} - {self.i18n.get('app.title')}")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        self.root.resizable(True, True)
        
        try:
            icon_path = Path(__file__).parent.parent / "files" / "pics" / "logo.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Текстовое меню с названием программы
        title_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="PyFusion 1.4" + (" + Kit" if KIT_AVAILABLE else ""), menu=title_menu)
        title_menu.add_command(label="About", command=self.show_about)
        title_menu.add_separator()
        title_menu.add_command(label="Developer Console", command=self.open_dev_console)
        title_menu.add_separator()
        title_menu.add_command(label="Exit", command=self.on_close)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("menu.file"), menu=file_menu)
        file_menu.add_command(label=self.i18n.get("menu.new"), 
                            command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label=self.i18n.get("menu.open"),
                            command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label=self.i18n.get("menu.save"),
                            command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label=self.i18n.get("menu.save_as"),
                            command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Close Tab", command=self.close_current_tab, accelerator="Ctrl+W")
        file_menu.add_separator()
        file_menu.add_command(label=self.i18n.get("menu.exit"),
                            command=self.on_close)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("menu.edit"), menu=edit_menu)
        edit_menu.add_command(label=self.i18n.get("menu.undo"),
                            command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label=self.i18n.get("menu.redo"),
                            command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label=self.i18n.get("menu.cut"),
                            command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label=self.i18n.get("menu.copy"),
                            command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label=self.i18n.get("menu.paste"),
                            command=self.paste, accelerator="Ctrl+V")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Editor", command=self.open_editor_tab)
        view_menu.add_command(label="File Creator", command=self.open_file_creator_tab)
        view_menu.add_command(label="Icon Tools", command=self.open_icon_tools_tab)
        view_menu.add_command(label="Package Manager", command=self.open_package_manager_tab)
        
        # Kit menu
        if KIT_AVAILABLE and self.kit:
            kit_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Kit", menu=kit_menu)
            kit_menu.add_command(label="Templates", command=self.open_templates_tab)
            kit_menu.add_command(label="Git Manager", command=self.open_git_tab)
            kit_menu.add_command(label="Archiver", command=self.open_archiver_tab)
            kit_menu.add_command(label="Advanced Icons", command=self.open_advanced_icons_tab)
            kit_menu.add_command(label="PyInstaller Pro", command=self.open_pyinstaller_tab)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("menu.tools"), menu=tools_menu)
        tools_menu.add_command(label=self.i18n.get("menu.settings"),
                             command=self.open_settings, accelerator="Ctrl+,")
        
        # Plugins menu
        if self.plugin_manager:
            plugins_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Plugins", menu=plugins_menu)
            
            if self.plugin_installer:
                plugins_menu.add_command(label="Plugin Installer", 
                                        command=self.plugin_installer.open_installer)
                plugins_menu.add_separator()
            
            plugin_items = self.plugin_manager.get_plugin_menu_items()
            if plugin_items:
                for item in plugin_items:
                    plugins_menu.add_command(
                        label=item.get("label", "Plugin"),
                        command=item.get("command")
                    )
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.i18n.get("menu.help"), menu=help_menu)
        help_menu.add_command(label=self.i18n.get("menu.about"),
                            command=self.show_about)
        
    def create_ui(self):
        """Создание основного интерфейса с вкладками"""
        # Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Приветственная вкладка
        self.create_welcome_tab()
        
        # Статус бар
        self.status_label = ttk.Label(self.root, text=self.i18n.get("status.ready"),
                                      relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Привязываем событие клика по вкладке для закрытия через крестик
        self.notebook.bind('<Button-1>', self.on_tab_click)
    
    def on_tab_click(self, event):
        """Обработка клика по вкладке для закрытия через крестик"""
        # Получаем вкладку под курсором
        tab_id = self.notebook.identify(event.x, event.y)
        if 'tab' not in tab_id:
            return
        
        # Получаем индекс вкладки
        tab_index = int(tab_id.split('tab')[1])
        tab_text = self.notebook.tab(tab_index, "text")
        
        # Не даём закрыть вкладку Welcome
        if tab_text == "Welcome":
            return
        
        # Получаем координаты и размеры вкладки
        tab_bbox = self.notebook.bbox(tab_index)
        
        if tab_bbox:
            # Область для крестика (правый край вкладки)
            close_x = tab_bbox[0] + tab_bbox[2] - 18
            close_y = tab_bbox[1] + 5
            
            # Проверяем, попали ли мы по крестику
            if close_x - 5 <= event.x <= close_x + 15 and close_y <= event.y <= close_y + 15:
                self.close_tab_by_index(tab_index)
    
    def close_tab_by_index(self, tab_index):
        """Закрыть вкладку по индексу"""
        tab_text = self.notebook.tab(tab_index, "text")
        
        # Не даём закрыть вкладку Welcome
        if tab_text == "Welcome":
            return
        
        # Получаем фрейм вкладки
        tab_frame = self.notebook.nametowidget(self.notebook.tabs()[tab_index])
        unsaved = False
        
        # Ищем редактор во вкладке
        for child in tab_frame.winfo_children():
            if hasattr(child, 'text') and hasattr(child, 'current_file'):
                content = child.text.get(1.0, tk.END).strip()
                if content:
                    unsaved = True
                    break
        
        if unsaved:
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"Tab '{tab_text}' has unsaved changes.\n\nYes - Save and close\nNo - Close without saving\nCancel - Don't close"
            )
            if result is None:
                return
            elif result:
                if self.current_editor:
                    self.current_editor.save_file()
        
        # Закрываем вкладку
        self.notebook.forget(tab_index)
        log_debug(f"Closed tab: {tab_text}")
        
        # Если закрыли редактор, обнуляем ссылку
        if tab_text == "Editor":
            self.current_editor = None
    
    def create_welcome_tab(self):
        """Создать приветственную вкладку"""
        welcome_frame = ttk.Frame(self.notebook)
        
        # Заголовок
        title_frame = ttk.Frame(welcome_frame)
        title_frame.pack(pady=(40, 10))
        
        try:
            logo_path = Path(__file__).parent.parent / "files" / "pics" / "logo_no_bg.png"
            if logo_path.exists() and PIL_AVAILABLE:
                img = Image.open(logo_path)
                new_width = 250
                new_height = int(1393 * (new_width / 2037))
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.big_logo = ImageTk.PhotoImage(img_resized)
                logo_label = ttk.Label(title_frame, image=self.big_logo)
                logo_label.pack(pady=5)
        except Exception as e:
            log_debug(f"Logo error: {e}")
        
        welcome_label = ttk.Label(title_frame, 
                                  text=self.i18n.get("app.welcome"),
                                  font=('TkDefaultFont', 18, 'bold'))
        welcome_label.pack()
        
        ttk.Label(welcome_frame, text="Select a tool from the menu or use shortcuts:",
                 font=('TkDefaultFont', 11)).pack(pady=10)
        
        # Shortcuts
        shortcuts_frame = ttk.LabelFrame(welcome_frame, text=" Shortcuts ", padding=10)
        shortcuts_frame.pack(pady=15, padx=50, fill=tk.X)
        
        shortcuts = [
            ("Ctrl+N", "New File"), ("Ctrl+O", "Open File"), ("Ctrl+S", "Save"),
            ("Ctrl+W", "Close Tab"), ("Ctrl+Z", "Undo"), ("Ctrl+Y", "Redo"),
            ("Ctrl+,", "Settings"),
        ]
        
        for i, (key, desc) in enumerate(shortcuts):
            ttk.Label(shortcuts_frame, text=f"{key}: {desc}",
                     font=('TkDefaultFont', 10)).grid(row=i//3, column=i%3, padx=20, pady=3, sticky=tk.W)
        
        # Кнопки
        quick_frame = ttk.Frame(welcome_frame)
        quick_frame.pack(pady=20)
        ttk.Button(quick_frame, text="New File", command=self.new_file, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Open File", command=self.open_file, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Open Editor", command=self.open_editor_tab, width=15).pack(side=tk.LEFT, padx=5)
        
        # Статус
        status_frame = ttk.Frame(welcome_frame)
        status_frame.pack(pady=20)
        
        if KIT_AVAILABLE:
            ttk.Label(status_frame, text="Kit: Activated",
                     font=('TkDefaultFont', 10), foreground='#4ec9b0').pack(side=tk.LEFT, padx=10)
        else:
            ttk.Label(status_frame, text="Kit: Not activated",
                     font=('TkDefaultFont', 10), foreground='#f48771').pack(side=tk.LEFT, padx=10)
        
        self.notebook.add(welcome_frame, text="Welcome")
    
    def add_tab(self, title, content_widget):
        """Добавить новую вкладку"""
        self.notebook.add(content_widget, text=title)
        self.notebook.select(content_widget)
        self.tab_frames[content_widget] = title
    
    def close_current_tab(self):
        """Закрыть текущую вкладку (Ctrl+W или меню)"""
        current = self.notebook.select()
        if current:
            tab_index = self.notebook.index(current)
            self.close_tab_by_index(tab_index)
    
    def open_dev_console(self):
        """Открыть консоль разработчика"""
        from utils.debug import get_debugger
        debugger = get_debugger()
        debugger.open_console(self)
    
    def open_editor_tab(self):
        """Открыть редактор"""
        # Проверяем, может уже есть открытый редактор
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "Editor":
                self.notebook.select(tab_id)
                return
        
        frame = ttk.Frame(self.notebook)
        editor = CodeEditor(frame, self)
        editor.pack(fill=tk.BOTH, expand=True)
        self.current_editor = editor
        self.add_tab("Editor", frame)
    
    def open_templates_tab(self):
        if self.kit:
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == "Templates":
                    self.notebook.select(tab_id)
                    return
            frame = ttk.Frame(self.notebook)
            self.kit.open_templates_in_frame(frame)
            self.add_tab("Templates", frame)

    def open_git_tab(self):
        if self.kit:
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == "Git":
                    self.notebook.select(tab_id)
                    return
            frame = ttk.Frame(self.notebook)
            self.kit.open_git_in_frame(frame)
            self.add_tab("Git", frame)

    def open_archiver_tab(self):
        if self.kit:
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == "Archiver":
                    self.notebook.select(tab_id)
                    return
            frame = ttk.Frame(self.notebook)
            self.kit.open_archiver_in_frame(frame)
            self.add_tab("Archiver", frame)

    def open_advanced_icons_tab(self):
        if self.kit:
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == "Advanced Icons":
                    self.notebook.select(tab_id)
                    return
            frame = ttk.Frame(self.notebook)
            self.kit.open_advanced_icons_in_frame(frame)
            self.add_tab("Advanced Icons", frame)

    def open_pyinstaller_tab(self):
        if self.kit:
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == "PyInstaller":
                    self.notebook.select(tab_id)
                    return
            frame = ttk.Frame(self.notebook)
            self.kit.open_pyinstaller_in_frame(frame)
            self.add_tab("PyInstaller", frame)
    
    def open_file_creator_tab(self):
        """Открыть создание файлов"""
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "File Creator":
                self.notebook.select(tab_id)
                return
        frame = ttk.Frame(self.notebook)
        creator = FileCreator(frame, self)
        creator.pack(fill=tk.BOTH, expand=True)
        self.add_tab("File Creator", frame)
    
    def open_icon_tools_tab(self):
        """Открыть инструменты иконок"""
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "Icon Tools":
                self.notebook.select(tab_id)
                return
        frame = ttk.Frame(self.notebook)
        tools = IconTools(frame, self)
        tools.pack(fill=tk.BOTH, expand=True)
        self.add_tab("Icon Tools", frame)
    
    def open_package_manager_tab(self):
        """Открыть менеджер пакетов"""
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, "text") == "Package Manager":
                self.notebook.select(tab_id)
                return
        frame = ttk.Frame(self.notebook)
        manager = PackageManager(frame, self)
        manager.pack(fill=tk.BOTH, expand=True)
        self.add_tab("Package Manager", frame)
    
    def bind_hotkeys(self):
        """Привязка горячих клавиш"""
        self.root.bind_all('<Control-n>', lambda e: self.new_file())
        self.root.bind_all('<Control-N>', lambda e: self.new_file())
        self.root.bind_all('<Control-o>', lambda e: self.open_file())
        self.root.bind_all('<Control-O>', lambda e: self.open_file())
        self.root.bind_all('<Control-s>', lambda e: self.save_file())
        self.root.bind_all('<Control-S>', lambda e: self.save_file_as())
        self.root.bind_all('<Control-w>', lambda e: self.close_current_tab())
        self.root.bind_all('<Control-W>', lambda e: self.close_current_tab())
        self.root.bind_all('<Control-comma>', lambda e: self.open_settings())
        self.root.bind_all('<Control-z>', lambda e: self.undo())
        self.root.bind_all('<Control-Z>', lambda e: self.undo())
        self.root.bind_all('<Control-y>', lambda e: self.redo())
        self.root.bind_all('<Control-Y>', lambda e: self.redo())
        self.root.bind_all('<Control-x>', lambda e: self.cut())
        self.root.bind_all('<Control-X>', lambda e: self.cut())
        self.root.bind_all('<Control-c>', lambda e: self.copy())
        self.root.bind_all('<Control-C>', lambda e: self.copy())
        self.root.bind_all('<Control-v>', lambda e: self.paste())
        self.root.bind_all('<Control-V>', lambda e: self.paste())
    
    def new_file(self):
        if not self.current_editor:
            self.open_editor_tab()
        if self.current_editor:
            self.current_editor.new_file()
    
    def open_file(self):
        if not self.current_editor:
            self.open_editor_tab()
        if self.current_editor:
            self.current_editor.open_file()
    
    def save_file(self):
        if self.current_editor:
            self.current_editor.save_file()
    
    def save_file_as(self):
        if self.current_editor:
            self.current_editor.save_as()
        else:
            self.open_editor_tab()
    
    def undo(self):
        if self.current_editor and hasattr(self.current_editor, 'text'):
            try:
                self.current_editor.text.edit_undo()
            except:
                pass
    
    def redo(self):
        if self.current_editor and hasattr(self.current_editor, 'text'):
            try:
                self.current_editor.text.edit_redo()
            except:
                pass
    
    def cut(self):
        if self.current_editor and hasattr(self.current_editor, 'text'):
            try:
                self.current_editor.text.event_generate("<<Cut>>")
            except:
                pass
    
    def copy(self):
        if self.current_editor and hasattr(self.current_editor, 'text'):
            try:
                self.current_editor.text.event_generate("<<Copy>>")
            except:
                pass
    
    def paste(self):
        if self.current_editor and hasattr(self.current_editor, 'text'):
            try:
                self.current_editor.text.event_generate("<<Paste>>")
            except:
                pass
    
    def open_settings(self):
        if self.settings.show_dialog():
            self.config.save()
    
    def set_status(self, text):
        if hasattr(self, 'status_label'):
            self.status_label.config(text=text)
    
    def show_about(self):
        plugin_count = len(self.plugin_manager.plugins) if self.plugin_manager else 0
        about_text = f"PyFusion 1.4\n\n"
        about_text += f"Kit: {'Activated' if KIT_AVAILABLE else 'Not activated'}\n"
        about_text += f"Plugins: {plugin_count}\n\n"
        about_text += "Copyright 2026 PyFusion Team"
        
        messagebox.showinfo("About PyFusion", about_text)
    
    def on_close(self):
        self.window_manager.close_all_windows()
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


def main():
    app = PyFusionApp()
    app.run()


if __name__ == "__main__":
    main()
