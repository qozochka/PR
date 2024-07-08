from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox


class ImageProcessor:
    def __init__(self):
        self.original_img = None
        self.current_img = None
        self.img_label = None
        self.img_tk = None

    def open_image(self, root):
        """
        Открывает изображения
        :param root: приложение
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.original_img = Image.open(file_path)
                self.current_img = self.original_img
                self.show_image(root)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Failed to open image: {e}")

    def show_image(self, root):
        """
        Отображает изображение при открытии
        :param root: приложение
        """
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
        """
        Отображает цветовой канал оригинального изображения
        :param channel: цветовой канал
        :param root: приложение
        """
        if not self.original_img:
            messagebox.showwarning("Ошибка", "Откройте изображение перед просмотром цветового канала.")
            return

        if self.original_img.mode == 'RGB':
            r, g, b = self.original_img.split()
        elif self.original_img.mode == 'L':
            r = g = b = self.original_img.copy()
        else:
            messagebox.showerror("Ошибка", "Выбранное изображение не является трехканальным (RGB)")
            return

        if channel == 'Красный':
            img = r
        elif channel == 'Зелёный':
            img = g
        elif channel == 'Синий':
            img = b
        else:
            img = r

        if self.img_label:
            self.img_label.destroy()

        img.thumbnail((600, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.current_img = img

        self.img_label = tk.Label(root.content_frame, image=self.img_tk)
        self.img_label.image = self.img_tk
        self.img_label.pack(pady=20)

    def show_negative(self, root):
        """
        Отображает негатив текущего изображения
        :param root:
        :return:
        """
        if not self.original_img:
            messagebox.showwarning("Ошибка", "Откройте изображение перед просмотром негативного изображения.")
            return

        img = ImageOps.invert(self.current_img.convert('RGB'))
        self.current_img = img

        if self.img_label:
            self.img_label.destroy()

        img.thumbnail((600, 400))
        self.img_tk = ImageTk.PhotoImage(img)

        self.img_label = tk.Label(root.content_frame, image=self.img_tk)
        self.img_label.image = self.img_tk
        self.img_label.pack(pady=20)

    def increase_brightness(self, value, root):
        """
        Повышает яркость на выбранный пользователем уровень
        :param value: значение выбранное пользователем на которое произойдет изменение яркости
        :param root: приложение
        """
        if not self.original_img:
            messagebox.showwarning("Ошибка", "Откройте изображение перед увеличением яркости.")
            return

        try:
            enhancer = ImageEnhance.Brightness(self.current_img)
            img = enhancer.enhance(value)
            self.current_img = img

            if self.img_label:
                self.img_label.destroy()

            img.thumbnail((600, 400))
            self.img_tk = ImageTk.PhotoImage(img)

            self.img_label = tk.Label(root.content_frame, image=self.img_tk)
            self.img_label.image = self.img_tk
            self.img_label.pack(pady=20)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось увеличить яркость: {e}")

    def draw_circle(self, x, y, radius, root):
        """
        Рисует красный круг поверх текущего изображения
        :param x: горизонтальная координата
        :param y: вертикальная координата
        :param radius: радиус
        :param root: приложение
        """
        if not self.original_img:
            messagebox.showwarning("Ошибка", "Откройте изображение перед рисованием круга.")
            return

        try:
            img = self.current_img.copy()
            draw = ImageDraw.Draw(img)

            if x - radius < 0 or y - radius < 0 or x + radius > img.width or y + radius > img.height:
                raise ValueError("Круг выходит за пределы изображения.")

            draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="red", fill="red", width=3)
            self.original_img = img
            self.current_img = img
            self.show_image(root)
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Не удалось нарисовать круг: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось нарисовать круг: {e}")
