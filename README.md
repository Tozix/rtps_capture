## Тестовое задание

___
### Описание
Данное приложение на Python в рамках тестового задания. 

### Возможности приложения
- Захват RTSP потока
- Захвата потока с web-камеры
- Сжатие полученного видеофайла
- Очистка от "мусорных кадров"


### Технологии
- [OpenCV]
- [python-ffmpeg]
___



### Запуск приложения в dev-режиме

- Клонировать репозиторий.

```bash

git clone git@github.com:Tozix/rtps_capture.git

```

- Установить и активировать виртуальное окружение c учетом версии Python 3.10

```bash

python3.10 -m venv venv

venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

```
### Установка ffmpeg на Ubuntu
```bash
sudo apt-get install -y software-properties-common
add apt-repository ppa:mc3man/trusty-media
apt-get update
apt-get dist-upgrade
apt-get install ffmpeg
```

### RTSP URL для теста

- rtsp://zephyr.rtsp.stream/movie?streamKey=5d13ef9c607f307c62cf728b165a14ac
- http://46.229.128.35:81/mjpg/video.mjpg'

### Запуск приложения
```bash
python main.py -s rtsp://zephyr.rtsp.stream/movie?streamKey=5d13ef9c607f307c62cf728b165a14ac -d 600
```
### Аргументы коммандной строки
```bash
options:
  -h, --help            show this help message and exit
  --stream STREAM, -s STREAM
                        URL RTSP потока
  --duration DURATION, -d DURATION
                        Продолжительность видеозахвата в секундах
  --demo_window, -w     Отображать видео в процессе захвата
```
### Утилиты
Написано 3 фунции обертки, для ffmpeg.
```bash
from utils import ffmpeg

convert_video(video_input, output_format):
"""Простая конвертация видеофайлов"""

compress_video(video_input, vcodec='libx265', crf=28):
"""Сжатие видео.
vcodec - Видео кодек
crf - Коэффициент постоянной скорости
"""
speedup_video(video_input, pts_cof=1, fps=30):
"""Ускорение видео.
Нормализация кол-во кадров в видео.
Нужна при многопоточном захвате.
Убирает дубликаты кадров.
"""
```

### To Do List
- Доработать многопоточную версию приложения
- Доработать обертку для ffmpeg




[//]: # (Ниже находятся справочные ссылки)

   [OpenCV]: <https://pypi.org/project/opencv-python/>
   [python-ffmpeg]: <https://pypi.org/project/python-ffmpeg/>
