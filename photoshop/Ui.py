import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from photoshop.Image import ImageProcessor
from photoshop.DrawCircleDialog import CircleDialog


class ImageProcessingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniPhotoshop")
        self.root.geometry("850x650")
        self.root.resizable(False, False)

        self.processor = ImageProcessor()

        self.camera = None
        self.frame = None  # Хранит текущий кадр камеры
        self.img_tk = None

        # Фрейм для кнопок
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.button_frame_2 = tk.Frame(self.root)
        self.button_frame_2.pack(side=tk.BOTTOM, fill=tk.X)

        # Разделитель между верхней полосой с кнопками и основной частью приложения
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Кнопка для открытия изображения
        self.open_img_btn = tk.Button(self.button_frame, text="Открыть фото",
                                      command=lambda: self.open_image(self))
        self.open_img_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для открытия камеры
        self.open_camera_btn = tk.Button(self.button_frame, text="Открыть камеру", command=self.open_camera)
        self.open_camera_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для сделать снимок
        self.snapshot_btn = tk.Button(self.button_frame, text="Сделать снимок", command=self.take_snapshot)
        self.snapshot_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопки для отображения цветовых каналов
        self.red_channel_btn = tk.Button(self.button_frame, text="Показать Красный канал",
                                         command=lambda: self.show_color_channel('Красный', self))
        self.red_channel_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.green_channel_btn = tk.Button(self.button_frame, text="Показать Зелёный канал",
                                           command=lambda: self.show_color_channel('Зелёный', self))
        self.green_channel_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.blue_channel_btn = tk.Button(self.button_frame, text="Показать Синий канал",
                                          command=lambda: self.show_color_channel('Синий', self))
        self.blue_channel_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопки для негатива и яркости
        self.negative_btn = tk.Button(self.button_frame_2, text="Показать Негатив", command=self.show_negative)
        self.negative_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.brightness_label = tk.Label(self.button_frame_2, text="Яркость:")
        self.brightness_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.brightness_scale = tk.Scale(self.button_frame_2, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.brightness_scale.set(1.0)
        self.brightness_scale.pack(side=tk.LEFT, padx=10, pady=10)

        self.brightness_btn = tk.Button(self.button_frame_2, text="Повысить яркость", command=self.increase_brightness)
        self.brightness_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для рисования круга
        self.draw_circle_btn = tk.Button(self.button_frame_2, text="Нарисовать круг", command=self.open_circle_dialog)
        self.draw_circle_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Фрейм для отображения
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        # Разделитель между верхней полосой с кнопками и основной частью приложения
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Label для отображения камеры
        self.snapshot_label = tk.Label(self.content_frame)
        self.snapshot_label.pack(pady=20)

    def open_camera(self):
        """
        Получает доступ к камере
        """
        self.close_camera()

        if self.snapshot_label:
            self.snapshot_label.destroy()
            self.snapshot_label = None

        if self.processor.img_label:
            self.processor.img_label.destroy()
            self.processor.img_label = None

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            messagebox.showerror("Ошибка", "Не удалось открыть камеру.")
            return

        self.show_camera_feed()

    def show_color_channel(self, channel, root):
        if self.camera:
            messagebox.showerror("Ошибка", "Сначала закройте камеру")
            return
        self.processor.show_color_channel(channel, root)

    def open_image(self, root):
        if self.camera:
            messagebox.showerror("Ошибка", "Сначала закройте камеру")
            return
        self.processor.open_image(root)

    def show_camera_feed(self):
        """
        Отображает камеру
        """
        if self.camera:
            _, frame = self.camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = Image.fromarray(frame)
            self.img_tk = ImageTk.PhotoImage(image=self.frame)

            if not self.snapshot_label:
                self.snapshot_label = tk.Label(self.content_frame)
                self.snapshot_label.pack(pady=20)

            self.snapshot_label.configure(image=self.img_tk)
            self.snapshot_label.image = self.img_tk

            self.root.after(10, self.show_camera_feed)

    def close_camera(self):
        if self.camera:
            self.camera.release()
            self.camera = None

    def take_snapshot(self):
        if self.frame:
            file_path = "snapshot.png"
            try:
                self.frame.save(file_path)
                self.close_camera()
                messagebox.showinfo("Инфо", f"Снимок сохранен как {file_path}")

                if self.snapshot_label:
                    self.snapshot_label.destroy()

                self.processor.original_img = Image.open(file_path)
                self.processor.current_img = Image.open(file_path)

                self.processor.show_image(self)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить снимок: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Сначала откройте камеру.")

    def show_negative(self):
        if self.camera:
            messagebox.showerror("Ошибка", "Сначала закройте камеру")
            return
        self.processor.show_negative(self)

    def increase_brightness(self):
        if self.camera:
            messagebox.showerror("Ошибка", "Сначала закройте камеру")
            return
        value = self.brightness_scale.get()
        self.processor.increase_brightness(value, self)

    def open_circle_dialog(self):
        if self.camera:
            messagebox.showerror("Ошибка", "Сначала закройте камеру")
            return
        self.root.attributes("-disabled", True)
        dialog = CircleDialog(self.root, title="Введите параметры круга")
        if dialog.x is not None and dialog.y is not None and dialog.radius is not None:
            self.processor.draw_circle(dialog.x, dialog.y, dialog.radius, self)
        self.root.attributes("-disabled", False)
