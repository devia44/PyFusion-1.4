#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for creating .pfp plugin file
"""

import json
import zipfile
import os
from pathlib import Path

def build_plugin():
    """Build the plugin into a .pfp file"""
    
    # Read manifest
    with open('manifest.json', 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    plugin_id = manifest.get('id', 'my_plugin')
    version = manifest.get('version', '1.0.0')
    
    output_file = f"{plugin_id}-v{version}.pfp"
    
    # Files to include
    files_to_include = [
        'manifest.json',
        'main.py',
        '__init__.py',
    ]
    
    # Optional files
    optional_files = ['README.md', 'LICENSE', 'icon.png']
    for file in optional_files:
        if os.path.exists(file):
            files_to_include.append(file)
    
    # Create zip
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files_to_include:
            if os.path.exists(file):
                zf.write(file)
                print(f"  Added: {file}")
    
    print(f"\nPlugin built: {output_file}")
    print(f"Size: {os.path.getsize(output_file)} bytes")

if __name__ == "__main__":
    build_plugin()
