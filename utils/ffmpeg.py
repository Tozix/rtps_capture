import itertools
import os
import sys

import ffmpeg

spinner = itertools.cycle(['-', '/', '|', '\\'])


def convert_video(video_input, output_format):
    """Простая конвертация видеофайлов"""
    file, ext = video_input.split('.')
    process = (
        ffmpeg
        .input(f'{file}.{ext}')
        .output(f'{file}.{output_format}')
        .overwrite_output()
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    while process.poll() is None:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
    os.remove(video_input)
    return str(f'{file}.{output_format}')


def compress_video(video_input, vcodec='libx265', crf=28):
    """Сжатие видео.
    vcodec - Видео кодек
    crf - Коэффициент постоянной скорости
    """
    file, _ = video_input.split('.')
    process = (
        ffmpeg
        .input(video_input)
        .output(f'{file}_compressed.mp4', vcodec=vcodec, crf=crf)
        .overwrite_output()
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )
    while process.poll() is None:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
    os.remove(video_input)
    os.rename(f'{file}_compressed.mp4', f'{file}.mp4')
    return str(f'{file}.mp4')


def speedup_video(video_input, pts_cof=1, fps=30):
    """Ускорение видео.
    Нормализация кол-во кадров в видео.
    Нужна при многопоточном захвате.
    Убирает дубликаты кадров.
    """
    file, _ = video_input.split('.')
    process = (
        ffmpeg
        .input(video_input)
        .output(f'{file}_sp.mp4', r=30, vf=f'setpts=PTS/{pts_cof}')
        .overwrite_output()
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    while process.poll() is None:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
    os.remove(video_input)
    os.rename(f'{file}_sp.mp4', f'{file}.mp4')
    return str(f'{file}.mp4')
