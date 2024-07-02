import tkinter as tk
from tkinter import filedialog, messagebox
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

    def open_image(self):
        self.processor.open_image()
        self.processor.show_image(self)

    def show_red_channel(self):
        self.processor.show_red_channel(self)

    def show_green_channel(self):
        self.processor.show_green_channel(self)

    def show_blue_channel(self):
        self.processor.show_blue_channel(self)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingUI(root)
    root.mainloop()
