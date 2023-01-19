# Валится видеозахват с ошибкой сегментирования. Фоновый процесс корректно не закрывается! Как правильно убить процесс ffmpeg вызванный VideoCapture ума не приложу!
from threading import Thread
import cv2


class VideoGet:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        (self.status, self.frame) = self.capture.read()
        self.stopped = False

    def start(self):
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def stop(self):
        self.capture.release()
        cv2.destroyAllWindows()
        self.stopped = True

    def update(self):
        while not self.stopped:
            if not self.status:
                self.stop()
            else:
                (self.status, self.frame) = self.capture.read()


class VideoShow:

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        self.thread = Thread(target=self.show, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self):
        self.stopped = True


class VideoWrite:

    def __init__(self, video_getter):
        capture = video_getter.capture
        self.frame = video_getter.frame
        self.frame_width = int(capture.get(
            cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(capture.get(
            cv2.CAP_PROP_FRAME_HEIGHT))
        self.filename = 'filename.avi'
        self.codec = cv2.VideoWriter_fourcc(*'XVID')
        self.output_video = cv2.VideoWriter(
            self.filename, self.codec, 30, (
                self.frame_width, self.frame_height))
        self.stopped = False

    def start(self):
        self.thread = Thread(target=self.write, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def write(self):
        while not self.stopped:
            self.output_video.write(self.frame)

    def stop(self):
        self.output_video.release()
        self.stopped = True


if __name__ == '__main__':
    src = 'rtsp://zephyr.rtsp.stream/movie?streamKey=5d13ef9c607f307c62cf728b165a14ac'
    video_getter = VideoGet(src).start()
    video_shower = VideoShow(video_getter.frame).start()
    video_writer = VideoWrite(video_getter).start()

    while video_getter.capture.isOpened():
        try:
            if video_getter.stopped or video_shower.stopped or video_writer.stopped:
                video_shower.stop()
                video_writer.stop()
                video_getter.stop()
                break
            else:
                frame = video_getter.frame
                video_writer.frame = frame
                video_shower.frame = frame

        except AttributeError:
            pass
