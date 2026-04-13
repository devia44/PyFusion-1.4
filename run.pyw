#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyFusion 1.3 - Multi-tool Development Environment
"""

import os
import sys
import tkinter as tk
from pathlib import Path
 
# Добавляем текущую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

# Пытаемся импортировать PIL для заставки
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def show_splash(duration=1500):
    """Показать заставку и запустить основное приложение"""
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.attributes('-topmost', True)
    splash.configure(bg='#1a1a1a')
    
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    
    # Путь к логотипу
    logo_path = Path(__file__).parent / "files" / "pics" / "logo.png"
    logo_path.parent.mkdir(parents=True, exist_ok=True)
    
    w, h = 400, 300
    
    if PIL_AVAILABLE and logo_path.exists():
        try:
            img = Image.open(logo_path)
            img.thumbnail((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(splash, image=photo, bg='#1a1a1a')
            label.image = photo  # Сохраняем ссылку
            label.pack()
            w, h = img.width, img.height
        except Exception:
            create_text_splash(splash)
    else:
        create_text_splash(splash)
    
    x = (screen_width - w) // 2
    y = (screen_height - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")
    
    # Функция запуска основного приложения
    def launch_main():
        splash.destroy()
        from core.app import PyFusionApp
        app = PyFusionApp()
        app.run()
    
    # Запускаем основное приложение после задержки
    splash.after(duration, launch_main)
    splash.mainloop()


def create_text_splash(splash):
    """Создание текстовой заставки"""
    frame = tk.Frame(splash, bg='#1a1a1a')
    frame.pack(expand=True, fill=tk.BOTH)
    
    title = tk.Label(frame, text="PyFusion", 
                    font=('Segoe UI', 36, 'bold'),
                    fg='#4ec9b0', bg='#1a1a1a')
    title.pack(pady=(50, 10))
    
    version = tk.Label(frame, text="Version 1.3",
                      font=('Segoe UI', 14),
                      fg='#888888', bg='#1a1a1a')
    version.pack()
    
    subtitle = tk.Label(frame, text="Loading...",
                       font=('Segoe UI', 10),
                       fg='#666666', bg='#1a1a1a')
    subtitle.pack(pady=20)
    
    splash.geometry("400x300")


if __name__ == "__main__":
    show_splash(2500)  # 2.5 секунды
