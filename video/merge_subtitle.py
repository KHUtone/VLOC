import subprocess

def merge_subtitle(videopath, subtitlepath, filename):
    command = "ffmpeg -i {} -c:v mpeg4 -q:v 1 -vf subtitles={} {}.mp4".format(videopath, subtitlepath, filename)
    subprocess.call(command, shell=True)
