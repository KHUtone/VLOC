# import moviepy.editor as mp
# clip = mp.VideoFileClip('test2.mp4').subclip(0,20)
# clip.audio.write_audiofile('test2.mp3')

import os
import subprocess

video_list = []
video_list = os.listdir('videos/')

#hard code
#video_list = ['video001.mp4']

for video in video_list:
    num = video.split('.')[0].replace('video','')
    command = "ffmpeg -i %s -ab 160k -ac 2 -ar 16000 -vn %s" % ('videos/'+video, 'audios/audio'+num+'.wav')
    subprocess.call(command, shell=True)

# from converter import Converter
# import os
# c = Converter()
# clip = 'test2.mp4'
# conv = c.convert(clip, 'audio2.mp3', {'format':'mp3','audio':{'codec': 'mp3','bitrate':'22050','channels':1}})
# for timecode in conv:
#     pass
# os.system("mpg123 -w audio2.wav audio2.mp3")
