import subprocess

'''
ffpeg commands
ffmpeg -i input.mp4 -an -vf setpts=PTS/4 result.mp4 - Ускорить видео
#Стриминг потока
ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 -f rtp_mpegts rtp://127.0.0.1:9999

'''


def convert_video(video_input, video_output):
    cmds = ['ffmpeg', '-i', video_input, video_output]
    subprocess.Popen(cmds)


def speedup_video(video_input, video_output, pts_cof=1):
    print('video_input', video_input)
    cmds = [
        'ffmpeg',
        '-i',
        video_input,
        '-an',
        '-vf',
        f'setpts=PTS/{pts_cof}',
        video_output
    ]
    subprocess.Popen(cmds)
