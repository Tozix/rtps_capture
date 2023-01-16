import logging
import os
from logging.handlers import RotatingFileHandler

import cv2

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
    '%(asctime)s [%(levelname)s] %(message)s %(funcName)s %(lineno)s'
)
file_log_handler.setFormatter(formatter)
console_out_handler.setFormatter(formatter)
logger.addHandler(file_log_handler)
logger.addHandler(console_out_handler)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

rtps = "rtp://127.0.0.1:9999"


def rtps_stream_capture(rtps, duration=120, output_file_path="output"):
    stream = cv2.VideoCapture(rtps)
    if not stream.isOpened():
        logger.error('Cannot open RTSP stream')
        exit(-1)
    stream_frame_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    stream_frame_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    stream_fps = int(stream.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    output = cv2.VideoWriter(
        f'{output_file_path}.avi', fourcc, stream_fps, (stream_frame_width, stream_frame_height))
    count_frame = 0
    while count_frame < stream_fps*duration:
        count_frame += 1
        stream_online, frame = stream.read()
        if not stream_online:
            logger.error('RTSP stream is closed')
            break
        try:
            output.write(frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.debug('Stoping capture on kepress')
                break
        except:
            break
    output.release()


def main():
    rtps_stream_capture(rtps)


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] %(funcName)s %(lineno)s %(message)s',
        filename='main.log', filemode='w',
        level=logging.INFO
    )
    try:
        main()
    except KeyboardInterrupt:
        logger.error('Keypress exit!')
        os._exit(1)
