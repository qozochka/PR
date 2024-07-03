import tkinter as tk
from tkinter import simpledialog, messagebox


class CircleDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.x = None
        self.y = None
        self.radius = None
        self.x_entry = None
        self.y_entry = None
        self.radius_entry = None
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Координата X:").grid(row=0)
        tk.Label(master, text="Координата Y:").grid(row=1)
        tk.Label(master, text="Радиус:").grid(row=2)

        self.x_entry = tk.Entry(master)
        self.y_entry = tk.Entry(master)
        self.radius_entry = tk.Entry(master)

        self.x_entry.grid(row=0, column=1)
        self.y_entry.grid(row=1, column=1)
        self.radius_entry.grid(row=2, column=1)

        return self.x_entry

    def apply(self):
        try:
            self.x = int(self.x_entry.get())
            self.y = int(self.y_entry.get())
            self.radius = int(self.radius_entry.get())
            if self.x < 0 or self.y < 0 or self.radius <= 0:
                raise ValueError("Координаты и радиус должны быть положительными числами.")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Пожалуйста, введите корректные значения: {e}")
            self.x = None
            self.y = None
            self.radius = None
