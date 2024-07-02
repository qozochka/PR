from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


class ImageProcessor:
    def __init__(self):
        self.original_img = None
        self.img_label = None
        self.img_tk = None

    def open_image(self, root):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.original_img = Image.open(file_path)
                self.show_image(root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

    def show_image(self, root):
        if self.img_label:
            self.img_label.destroy()

        if self.original_img:
            img = self.original_img.copy()
            img.thumbnail((600, 400))
            self.img_tk = ImageTk.PhotoImage(img)

            self.img_label = tk.Label(root.content_frame, image=self.img_tk)
            self.img_label.image = self.img_tk
            self.img_label.pack(pady=20)

    def show_color_channel(self, channel, root):
        if not self.original_img:
            messagebox.showwarning("Warning", "Откройте изображение перед просмотром цветового канала.")
            return

        if self.original_img.mode == 'RGB':
            r, g, b = self.original_img.split()
        elif self.original_img.mode == 'L':
            r = g = b = self.original_img.copy()
        else:
            messagebox.showerror("Error", "Выбранное изображение не является трехканальным (RGB)")
            return

        if channel == 'Красный':
            img = r
        elif channel == 'Зелёный':
            img = g
        elif channel == 'Синий':
            img = b

        if self.img_label:
            self.img_label.destroy()

        img.thumbnail((600, 400))
        self.img_tk = ImageTk.PhotoImage(img)

        self.img_label = tk.Label(root.content_frame, image=self.img_tk)
        self.img_label.image = self.img_tk
        self.img_label.pack(pady=20)