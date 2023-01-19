import argparse
import datetime
import decimal
import logging
import os
import time
from logging.handlers import RotatingFileHandler

import cv2 as cv

from utils import ffmpeg

VIDEOS_PATH = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_log_handler = RotatingFileHandler(
    filename='main.log',
    encoding='utf8',
    maxBytes=50000000,
    backupCount=5
)
console_out_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'
)
file_log_handler.setFormatter(formatter)
console_out_handler.setFormatter(formatter)
logger.addHandler(file_log_handler)
logger.addHandler(console_out_handler)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def stream_write(src=0, duration=10, demo=False):
    now = str(datetime.datetime.today().strftime("%Y-%m-%d-%H%M%S"))
    filename = f'{VIDEOS_PATH}/{now}.avi'
    capture = cv.VideoCapture(src)
    frame_count = 0
    frame_width = int(capture.get(
        cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(
        cv.CAP_PROP_FRAME_HEIGHT))
    codec = cv.VideoWriter_fourcc(*'XVID')
    output_video = cv.VideoWriter(
        filename, codec, 30, (
            frame_width, frame_height))

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            logger.error('Не смог получить кадр из потока')
            break
        if frame_count == 0:
            timeout = time.time()+duration
        if time.time() > timeout:
            logger.debug('Завершение видеозахвата по времени')
            break

        output_video.write(frame)
        frame_count += 1
        if demo:
            cv.imshow('Demo window', frame)
            if cv.waitKey(1) == ord('q'):
                logger.debug(
                    'Завершение видеозахвата по нажатию клавишы'
                )
                break
    else:
        logger.debug('Нет соединения с RTSP потоком')

    logger.debug(
        f'Кол-во записанных кадров: {frame_count}'
    )
    capture.release()
    output_video.release()
    cv.destroyAllWindows()
    refernce_frame_count = duration*30
    logger.debug(
        f'Ожидаемое кол-во кадров: {refernce_frame_count}'
    )
    diff_coef = frame_count/refernce_frame_count
    logger.debug(f'Коэффициент разницы: {diff_coef}')
    return filename, diff_coef


def round_up(num, place=0):
    """
    Округляет вещественные числа.
    place - число знаков после запятой
    """
    context = decimal.getcontext()
    original_rounding = context.rounding
    context.rounding = decimal.ROUND_CEILING
    rounded = round(decimal.Decimal(str(num)), place)
    context.rounding = original_rounding
    return float(rounded)


def get_size(file_path):
    """Возвращает размер файла в МБ"""
    size_in_bytes = os.path.getsize(file_path)
    return round_up((size_in_bytes/1024/1024), 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Справка:')
    parser.add_argument(
        "--stream",
        "-s",
        type=str,
        help="URL RTSP потока"
    )
    parser.add_argument(
        "--duration",
        "-d",
        type=int,
        help="Продолжительность видеозахвата в секундах"
    )
    parser.add_argument(
        "--demo_window",
        "-w",
        action='store_true',
        help="Отображать видео в процессе захвата"
    )
    args = parser.parse_args()

    if not args.stream:
        parser.error(
            'Не указан URL видеопотока! --stream STREAM'
        )
    video_filename, diff_coef = stream_write(
        args.stream, args.duration, args.demo_window
    )
    logger.debug(
        f'Размер полученного видео: {get_size(video_filename)} Мб'
    )
    if diff_coef > 1:
        logger.debug('Нормализуем кол-во кадров')
        video_filename = ffmpeg.speedup_video(video_filename, diff_coef)
        logger.debug(
            f'Размер видео после нормализации: {get_size(video_filename)} Мб'
        )
    new_video = ffmpeg.compress_video(video_filename)
    logger.debug('Сжатие видео')
    logger.debug(
        f'Размер видео после сжатия": {get_size(new_video)} Мб'
    )
