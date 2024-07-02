import tkinter as tk
from tkinter import messagebox
from PIL import ImageDraw, Image, ImageTk


class DrawCircleDialog:
    def __init__(self, root, processor):
        self.root = root
        self.top = tk.Toplevel(root)
        self.top.title("Введите параметры круга")
        self.top.geometry("150x250")

        self.processor = processor

        self.x_label = tk.Label(self.top, text="X:")
        self.x_label.pack(pady=5)
        self.x_entry = tk.Entry(self.top, width=10)
        self.x_entry.pack(pady=5)

        self.y_label = tk.Label(self.top, text="Y:")
        self.y_label.pack(pady=5)
        self.y_entry = tk.Entry(self.top, width=10)
        self.y_entry.pack(pady=5)

        self.radius_label = tk.Label(self.top, text="Радиус:")
        self.radius_label.pack(pady=5)
        self.radius_entry = tk.Entry(self.top, width=10)
        self.radius_entry.pack(pady=5)

        self.draw_btn = tk.Button(self.top, text="Нарисовать", command=self.draw_circle)
        self.draw_btn.pack(pady=10)

    def draw_circle(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            radius = int(self.radius_entry.get())
            self.processor.draw_circle(x, y, radius)
            self.top.destroy()  # Закрываем диалоговое окно после отрисовки круга
        except ValueError:
            messagebox.showerror("Error", "Введите корректные значения для X, Y и радиуса.")


