import logging
import os
import time
from logging.handlers import RotatingFileHandler
from threading import Thread

import cv2

from utils.ffmpeg import speedup_video

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


class RTSPVideoWriter(object):
    def __init__(self, src=0, duration=10, filename='output.avi'):
        self.capture = cv2.VideoCapture(src)
        self.duration = duration
        self.timeout = time.time()+duration
        self.frame_count = 0
        self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.filename = filename
        self.codec = cv2.VideoWriter_fourcc(*'MPEG')
        self.output_video = cv2.VideoWriter(
            self.filename, self.codec, 30, (self.frame_width, self.frame_height))
        self.working = True
        logger.debug('Запуск потока чтения кадров')
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        '''Покадрово читаем поток.'''
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        '''Демонстрация захваченного видеопотока в отдельном окне.
        Клавиша q, что бы завершить запись и демонстрацию
        '''
        if self.status:
            cv2.imshow('frame', self.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            self.working = False

    def stream_check(self):
        ''''''
        if not self.status:
            logger.error('Не смог получить кадр из потока')
            self.capture.release()
            self.output_video.release()
        if time.time() > self.timeout:
            logger.debug('Время вышло, закнчиваем запись!')
            self.capture.release()
            self.output_video.release()
            self.working = False

    def save_frame(self):
        '''Сохраняет полученный кадр в выходной видеофайл.'''
        self.frame_count += 1
        self.output_video.write(self.frame)


if __name__ == '__main__':
    # rtsp_stream = 'http://46.229.128.35:81/mjpg/video.mjpg'
    rtsp_stream = 'rtp://127.0.0.1:9999'
    duration = 30
    video_stream = RTSPVideoWriter(rtsp_stream, duration)
    while video_stream.working:
        try:
            video_stream.stream_check()
            # video_stream.show_frame()
            video_stream.save_frame()
        except AttributeError:
            pass
    else:
        logger.debug(f'Кол-во кадров: {video_stream.frame_count}')
    refernce_duration = duration*30
    print('Кол-во кажро', video_stream.frame_count)
    print('Коф. ускорения видео', video_stream.frame_count/refernce_duration)
    speedup_video(f'{VIDEOS_PATH}/output.avi', f'{VIDEOS_PATH}/result.avi',
                  video_stream.frame_count/refernce_duration)
