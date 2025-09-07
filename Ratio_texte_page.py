# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 10:56:41 2024

@author: aubin
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageRectangleSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Sélection de rectangles")
        
        self.canvas = tk.Canvas(root, cursor="cross", bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
  
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.image = None
        self.photo_image = None
        self.is_selecting_main_rectangle = True
        self.main_rectangle_area = 0
        self.small_rectangles_areas = []

        calculate_button = tk.Button(root, text="Calculer le ratio", command=self.calculate_ratio, width=15)
 
        reset_button = tk.Button(root, text="Réinitialiser la sélection", command=self.reset_selection, width=20)

        calculate_button.pack(side=tk.LEFT, padx=(100, 10), pady=10, ipadx=5, ipady=5)
        reset_button.pack(side=tk.LEFT, padx=(10, 100), pady=10, ipadx=5, ipady=5)
        
        self.open_image()

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            max_size = (1500, 1000)
            self.image.thumbnail(max_size, Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        outline_color = 'red' if self.is_selecting_main_rectangle else 'blue'
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline=outline_color)
    
    def on_mouse_drag(self, event):
        self.current_x, self.current_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.current_x, self.current_y)
    
    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        area = width * height

        if self.is_selecting_main_rectangle:
            self.main_rectangle_area = area
            self.is_selecting_main_rectangle = False
            print(f"Surface de la page: {area} pixels")
        else:
            self.small_rectangles_areas.append(area)
            print(f"Surface de poésie: {area} pixels")

        self.start_x, self.start_y, self.current_x, self.current_y = None, None, None, None
        self.rect = None 
    
    def calculate_ratio(self):
        if self.main_rectangle_area == 0:
            print("Veuillez d'abord sélectionner la taille de la page.")
            return
        
        total_small_area = sum(self.small_rectangles_areas)
        ratio = total_small_area / self.main_rectangle_area if self.main_rectangle_area > 0 else 0
        formatted_ratio = f"{ratio:.2f}"
        print(f"Ratio (texte poétique / page): {formatted_ratio}")
    
    def reset_selection(self):
        self.is_selecting_main_rectangle = True
        self.main_rectangle_area = 0
        self.small_rectangles_areas = []
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        print("Sélection réinitialisée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRectangleSelector(root)
    root.mainloop()
