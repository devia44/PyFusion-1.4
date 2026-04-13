# -*- coding: utf-8 -*-
"""
Упрощённая интернационализация — только английский
"""

class I18n:
    def __init__(self):
        self.current_language = "en"
    
    def get(self, key, default=None):
        """Возвращает английский текст по ключу"""
        strings = {
            # App
            "app.title": "Development Environment",
            "app.welcome": "Welcome to PyFusion 1.4",
            
            # Menu
            "menu.file": "File",
            "menu.edit": "Edit",
            "menu.view": "View",
            "menu.window": "Window",
            "menu.tools": "Tools",
            "menu.help": "Help",
            "menu.new": "New File",
            "menu.open": "Open...",
            "menu.save": "Save",
            "menu.save_as": "Save As...",
            "menu.close": "Close",
            "menu.exit": "Exit",
            "menu.undo": "Undo",
            "menu.redo": "Redo",
            "menu.cut": "Cut",
            "menu.copy": "Copy",
            "menu.paste": "Paste",
            "menu.settings": "Settings",
            "menu.about": "About",
            
            # Editor
            "editor.new": "New",
            "editor.open": "Open",
            "editor.save": "Save",
            "editor.run": "Run",
            "editor.new_file": "New file",
            "editor.opened": "Opened",
            "editor.saved": "Saved",
            "editor.save_first": "Save file first",
            "editor.output": "Output",
            "editor.timeout": "Execution timeout (30s)",
            
            # File Creator
            "creator.title": "Create File",
            "creator.filename": "Filename",
            "creator.extension": "Extension",
            "creator.content": "Content",
            "creator.create": "Create",
            "creator.clear": "Clear",
            "creator.success": "Success",
            "creator.created": "Created file",
            "creator.error_no_name": "Enter filename",
            
            # Package Manager
            "pkg.title": "Package Manager",
            "pkg.install": "Install",
            "pkg.uninstall": "Uninstall",
            "pkg.package_name": "Package name",
            "pkg.installed_packages": "Installed Packages",
            "pkg.refresh": "Refresh",
            
            # Settings
            "settings.title": "Settings",
            "settings.general": "General",
            "settings.language": "Language",
            "settings.theme": "Theme",
            "settings.save": "Save",
            "settings.cancel": "Cancel",
            
            # Status
            "status.ready": "Ready",
            
            # Windows
            "window.new_editor": "New Editor",
            "window.file_creator": "File Creator",
            "window.icon_tools": "Icon Tools",
            "window.package_manager": "Package Manager",
            "window.templates": "Templates",
            "window.tile": "Tile Windows",
            "window.cascade": "Cascade Windows",
            "window.close_all": "Close All Windows",
            "window.open_editor": "Open Editor",
            "window.open_file_creator": "Open File Creator",
            "window.open_icon_tools": "Open Icon Tools",
            "window.open_package_manager": "Open Package Manager",
            
            # Icon Tools
            "icon.png_to_ico": "Convert PNG to ICO",
            "icon.select_png": "Select PNG",
            "icon.convert": "Convert",
            "icon.set_folder_icon": "Set Folder Icon",
            "icon.select_folder": "Select Folder",
            "icon.select_ico": "Select ICO",
            "icon.apply": "Apply",
            "icon.success": "Success",
            "icon.created": "Created ICO file",
            "icon.applied": "Icon applied",
            
            # Templates
            "templates.title": "Code Templates",
            "templates.insert": "Insert",
            
            # About
            "about.title": "About PyFusion",
            
            # Kit
            "kit.templates": "Templates",
            "kit.git": "Git Manager",
            "kit.archiver": "Archiver",
            "kit.advanced_icons": "Advanced Icons",
            "kit.pyinstaller": "PyInstaller Pro",
        }
        
        return strings.get(key, default or key)
    
    def set_language(self, lang):
        self.current_language = "en"
        return True
    
    def get_available_languages(self):
        return ["en"]
