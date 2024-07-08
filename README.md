# Ознакомительная практика ИКИТ СФУ
## Задание:
### Разработать программу, включающую следующие функции:
- Загрузка изображений через проводник
- Захват изображения с веб-камеры
- Отображение изображения в окне приложения
- Отображение красного, зеленого или синего канала изображения по выбору пользователя
- Отображение негативного изображения
- Повышение яркости изображения
- Рисование красного круга на изображении, пользователь вводит характеристики круга

### При разработке программы использовались следующие дополнительные библиотеки:
- [OpenCv](https://opencv.org/) - для работы с коррекцией изображения
- [Pillow](https://pillow.readthedocs.io/en/stable/) - для создания графического интерфейса


### Инструкция по запуску программы:
1. Склонируйте удаленный репозиторий
```bash
git clone <URL репозитория>
    cd <имя репозитория>
```
2. Установите пакетный менеджер conda, если он не установлен.


3. Создайте виртуальное окружение и установите зависимости:

```bash
conda env create -f environment.yml
```
4. Активируйте созданное окружение:

```bash
conda activate env_name
```

5. Запустите приложение:

```bash
python main.py
```

