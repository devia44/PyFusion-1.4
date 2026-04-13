# -*- coding: utf-8 -*-
"""
Basic Icon Tools
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class IconTools(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI"""
        if not PIL_AVAILABLE:
            ttk.Label(self, text="PIL/Pillow not installed. Install: pip install Pillow",
                     foreground="red").pack(pady=20)
            return
        
        # Title
        title = ttk.Label(self, text="PNG to ICO Converter",
                         font=('TkDefaultFont', 14, 'bold'))
        title.pack(pady=15)
        
        # Main container
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Select PNG
        select_frame = ttk.LabelFrame(container, text="Select PNG File")
        select_frame.pack(fill=tk.X, pady=10)
        
        inner = ttk.Frame(select_frame)
        inner.pack(fill=tk.X, padx=10, pady=10)
        
        self.png_path = tk.StringVar()
        ttk.Entry(inner, textvariable=self.png_path).pack(side=tk.LEFT, 
                                                          fill=tk.X, expand=True)
        ttk.Button(inner, text="Browse", 
                  command=self.select_png).pack(side=tk.LEFT, padx=5)
        
        # Icon sizes
        sizes_frame = ttk.LabelFrame(container, text="Icon Sizes")
        sizes_frame.pack(fill=tk.X, pady=10)
        
        inner2 = ttk.Frame(sizes_frame)
        inner2.pack(fill=tk.X, padx=10, pady=10)
        
        self.sizes_vars = {}
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        
        for i, (w, h) in enumerate(sizes):
            var = tk.BooleanVar(value=(w in [32, 64, 128]))
            self.sizes_vars[(w,h)] = var
            ttk.Checkbutton(inner2, text=f"{w}x{w}", variable=var).grid(
                row=i//3, column=i%3, sticky=tk.W, padx=10, pady=2
            )
        
        # Set folder icon
        folder_frame = ttk.LabelFrame(container, text="Set Folder Icon")
        folder_frame.pack(fill=tk.X, pady=10)
        
        inner3 = ttk.Frame(folder_frame)
        inner3.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(inner3, text="Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(inner3, textvariable=self.folder_path)
        folder_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(inner3, text="Browse", 
                  command=self.select_folder).grid(row=0, column=2, padx=5)
        
        ttk.Label(inner3, text="Icon:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.folder_icon_path = tk.StringVar()
        icon_entry = ttk.Entry(inner3, textvariable=self.folder_icon_path)
        icon_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        ttk.Button(inner3, text="Browse", 
                  command=self.select_icon).grid(row=1, column=2, padx=5)
        
        inner3.columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Convert to ICO",
                  command=self.convert_to_ico, style="success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Apply Icon to Folder",
                  command=self.apply_folder_icon).pack(side=tk.LEFT, padx=5)
        
        # Kit info
        kit_frame = ttk.Frame(container)
        kit_frame.pack(pady=20)
        
        ttk.Label(kit_frame, 
                 text="PyFusion Kit adds:",
                 font=('TkDefaultFont', 9, 'bold'),
                 foreground='#4ec9b0').pack()
        
        ttk.Label(kit_frame,
                 text="• Convert any image (JPG, BMP, GIF, WEBP)",
                 font=('TkDefaultFont', 9),
                 foreground='#808080').pack()
        ttk.Label(kit_frame,
                 text="• Set icons for files and extensions",
                 font=('TkDefaultFont', 9),
                 foreground='#808080').pack()
        ttk.Label(kit_frame,
                 text="• Batch conversion",
                 font=('TkDefaultFont', 9),
                 foreground='#808080').pack()
        ttk.Label(kit_frame,
                 text="• Icon editor",
                 font=('TkDefaultFont', 9),
                 foreground='#808080').pack()
    
    def select_png(self):
        file = filedialog.askopenfilename(
            title="Select PNG file",
            filetypes=[("PNG files", "*.png")]
        )
        if file:
            self.png_path.set(file)
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            self.folder_path.set(folder)
    
    def select_icon(self):
        file = filedialog.askopenfilename(
            title="Select ICO file",
            filetypes=[("ICO files", "*.ico")]
        )
        if file:
            self.folder_icon_path.set(file)
    
    def convert_to_ico(self):
        if not self.png_path.get():
            messagebox.showerror("Error", "Select PNG file")
            return
        
        sizes = [size for size, var in self.sizes_vars.items() if var.get()]
        if not sizes:
            messagebox.showerror("Error", "Select at least one icon size")
            return
        
        output = filedialog.asksaveasfilename(
            defaultextension=".ico",
            filetypes=[("ICO files", "*.ico")]
        )
        
        if output:
            try:
                img = Image.open(self.png_path.get())
                img.save(output, format='ICO', sizes=sizes)
                messagebox.showinfo("Success", f"ICO created: {output}")
                if hasattr(self.app, 'set_status'):
                    self.app.set_status(f"ICO created: {os.path.basename(output)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def apply_folder_icon(self):
        folder = self.folder_path.get()
        icon = self.folder_icon_path.get()
        
        if not folder or not icon:
            messagebox.showerror("Error", "Select folder and icon")
            return
        
        try:
            import ctypes
            
            desktop_ini = os.path.join(folder, 'desktop.ini')
            with open(desktop_ini, 'w', encoding='utf-8') as f:
                f.write(f'[.ShellClassInfo]\nIconResource={icon},0\n')
            
            ctypes.windll.kernel32.SetFileAttributesW(folder, 0x02)
            ctypes.windll.kernel32.SetFileAttributesW(desktop_ini, 0x02)
            
            messagebox.showinfo("Success", "Icon applied to folder")
            if hasattr(self.app, 'set_status'):
                self.app.set_status("Icon applied")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_texts(self):
        pass
