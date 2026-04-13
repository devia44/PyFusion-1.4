# -*- coding: utf-8 -*-
"""
Конфигурация приложения
"""

import os
import json
from pathlib import Path


class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".pyfusion"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        
        self.defaults = {
            "language": "en",
            "theme": "darkly",
            "editor_font": "Consolas",
            "editor_font_size": 11,
            "auto_save": True,
            "recent_files": [],
            "max_recent_files": 10,
            "debug_max_size_mb": 1,  # Максимальный размер лога в МБ
            "debug_level": "INFO"     # DEBUG, INFO, WARNING, ERROR
        }
        
        self.data = self.load()
    
    def load(self):
        """Загрузка конфигурации"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {**self.defaults, **data}
            except:
                return self.defaults.copy()
        return self.defaults.copy()
    
    def save(self):
        """Сохранение конфигурации"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        """Получение значения"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Установка значения"""
        self.data[key] = value
        self.save()
    
    def add_recent_file(self, filepath):
        """Добавление файла в список недавних"""
        recent = self.data.get("recent_files", [])
        if filepath in recent:
            recent.remove(filepath)
        recent.insert(0, filepath)
        max_files = self.data.get("max_recent_files", 10)
        self.data["recent_files"] = recent[:max_files]
        self.save()
    
    def get_recent_files(self):
        """Получение списка недавних файлов"""
        return self.data.get("recent_files", [])
