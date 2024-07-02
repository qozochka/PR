import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from Image import ImageProcessor


class ImageProcessingUI:
    def __init__(self, root1):
        self.root = root1
        self.root.title("Image Processing Application")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.processor = ImageProcessor()

        # Фрейм для кнопок и контента
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        # Разделитель между верхней полосой с кнопками и основной частью приложения
        tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Кнопка для открытия изображения
        self.open_img_btn = tk.Button(self.button_frame, text="Открыть фото", command=self.open_image)
        self.open_img_btn.pack(side=tk.LEFT,
                               padx=10,
                               pady=10)

        # Кнопка для открытия камеры
        self.open_camera_btn = tk.Button(self.button_frame, text="Открыть камеру", command=self.open_camera)
        self.open_camera_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопка для сделать снимок
        self.snapshot_btn = tk.Button(self.button_frame, text="Сделать снимок", command=self.take_snapshot)
        self.snapshot_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Кнопки для отображения цветовых каналов
        self.red_channel_btn = tk.Button(self.button_frame,
                                         text="Показать Красный канал",
                                         command=self.show_red_channel)

        self.red_channel_btn.pack(side=tk.LEFT,
                                  padx=10,
                                  pady=10)

        self.green_channel_btn = tk.Button(self.button_frame,
                                           text="Показать Зелёный канал",
                                           command=self.show_green_channel)

        self.green_channel_btn.pack(side=tk.LEFT,
                                    padx=10,
                                    pady=10)

        self.blue_channel_btn = tk.Button(self.button_frame,
                                          text="Показать Синий канал",
                                          command=self.show_blue_channel)

        self.blue_channel_btn.pack(side=tk.LEFT,
                                   padx=10,
                                   pady=10)

        # Фрейм для отображения контента (изображений)
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        self.camera = None
        self.frame = None
        self.img_tk = None

        # Инициализация snapshot_label с пустым изображением
        self.snapshot_label = tk.Label(self.content_frame)
        self.snapshot_label.pack(pady=20)

    def open_camera(self):
        self.camera = cv2.VideoCapture(0)  # Открываем камеру с индексом 0 (обычно встроенная)

        if not self.camera.isOpened():
            messagebox.showerror("Error", "Не удалось открыть камеру.")
            return

        self.show_camera_feed()

    def show_camera_feed(self):
        _, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame = Image.fromarray(frame)

        self.update_snapshot_label()

    def update_snapshot_label(self):
        _, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame = Image.fromarray(frame)

        img_tk = ImageTk.PhotoImage(image=self.frame)

        if not self.snapshot_label:
            self.snapshot_label = tk.Label(self.content_frame)
            self.snapshot_label.pack(pady=20)

        self.snapshot_label.configure(image=img_tk)
        self.snapshot_label.image = img_tk


        # Вызываем update_snapshot_label() снова через 10 миллисекунд
        self.root.after(10, self.update_snapshot_label)

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

                # Загружаем сохраненное изображение в ImageProcessor
                self.processor.original_img = Image.open(file_path)
                # Отображаем сохраненное изображение в интерфейсе
                self.show_snapshot(file_path)

            except Exception as e:
                messagebox.showerror("Error", f"Не удалось сохранить снимок: {e}")
        else:
            messagebox.showwarning("Warning", "Сначала откройте камеру.")

    def open_image(self):
        self.processor.open_image()
        self.processor.show_image(self)

    def show_red_channel(self):
        self.processor.show_red_channel(self)

    def show_green_channel(self):
        self.processor.show_green_channel(self)

    def show_blue_channel(self):
        self.processor.show_blue_channel(self)

    def show_snapshot(self, file_path):
        img = Image.open(file_path)
        img.thumbnail((600, 400))
        img_tk = ImageTk.PhotoImage(image=img)

        if self.snapshot_label:
            self.snapshot_label.destroy()

        self.processor.img_label = tk.Label(self.content_frame, image=img_tk)
        self.processor.img_label.image = img_tk
        self.processor.img_label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingUI(root)
    root.mainloop()
