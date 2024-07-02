import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from Image import ImageProcessor


class ImageProcessingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.processor = ImageProcessor()

        self.camera = None
        self.frame = None
        self.img_tk = None

        # Фрейм для кнопок и контента
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        # Разделитель между верхней полосой с кнопками и основной частью приложения
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Кнопка для открытия изображения
        self.open_img_btn = tk.Button(self.button_frame, text="Открыть фото", command=lambda: self.processor.open_image(self))
        self.open_img_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для открытия камеры
        self.open_camera_btn = tk.Button(self.button_frame, text="Открыть камеру", command=self.open_camera)
        self.open_camera_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для сделать снимок
        self.snapshot_btn = tk.Button(self.button_frame, text="Сделать снимок", command=self.take_snapshot)
        self.snapshot_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопки для отображения цветовых каналов
        self.red_channel_btn = tk.Button(self.button_frame, text="Показать Красный канал", command=lambda: self.processor.show_color_channel('Красный', self))
        self.red_channel_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.green_channel_btn = tk.Button(self.button_frame, text="Показать Зелёный канал", command=lambda: self.processor.show_color_channel('Зелёный', self))
        self.green_channel_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.blue_channel_btn = tk.Button(self.button_frame, text="Показать Синий канал", command=lambda: self.processor.show_color_channel('Синий', self))
        self.blue_channel_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Фрейм для отображения контента (изображений)
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        # Label для отображения снимка с камеры
        self.snapshot_label = tk.Label(self.content_frame)
        self.snapshot_label.pack(pady=20)

    def open_camera(self):
        self.close_camera()

        if self.snapshot_label:
            self.snapshot_label.destroy()
            self.snapshot_label = None

        if self.processor.img_label:
            self.processor.img_label.destroy()
            self.processor.img_label = None

        self.camera = cv2.VideoCapture(0)  # Открываем камеру с индексом 0 (обычно встроенная)

        if not self.camera.isOpened():
            messagebox.showerror("Error", "Не удалось открыть камеру.")
            return

        self.show_camera_feed()

    def show_camera_feed(self):
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

            # Вызываем update_snapshot_label() снова через 10 миллисекунд
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
                self.close_camera()  # Закрываем камеру после сохранения снимка
                messagebox.showinfo("Info", f"Снимок сохранен как {file_path}")

                if self.snapshot_label:
                    self.snapshot_label.destroy()

                self.processor.original_img = Image.open(file_path)
                self.processor.show_image(self)

            except Exception as e:
                messagebox.showerror("Error", f"Не удалось сохранить снимок: {e}")
        else:
            messagebox.showwarning("Warning", "Сначала откройте камеру.")

