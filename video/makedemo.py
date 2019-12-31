import os
import cv2
import numpy as np
import shutil
from pydub import AudioSegment

def frames_to_video(inputpath,outputpath,fps):
   image_array = []
   files = []
   for path in inputpath:
       files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
   #files.sort(key = lambda x: int(x[5:-4]))
       for i in range(len(files)):
           img = cv2.imread(path + files[i])
           size =  (img.shape[1],img.shape[0])
           img = cv2.resize(img,size)
           image_array.append(img)
   fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
   out = cv2.VideoWriter(outputpath,fourcc, fps, size)
   for i in range(len(image_array)):
       out.write(image_array[i])
   out.release()

path = 'frames/video006'

folder_list = os.listdir(path)
# for i, folder in enumerate(folder_list):
#     folder_list[i] = path + '/' + folder + '/'
#
# print(folder_list)

f = open ('frames/labels/video006.txt')
lines = f.readlines()

lines_ = []
lines2 = []
for i, line in enumerate(lines):
    splited = line.replace('\n','').split()
    if splited[1] == '5':
        lines_.append(splited[0])
        lines2.append(splited[0])
f.close()

#print(lines_)
folders = lines_
for i, item in enumerate(folders):
    folders[i] = path + '/' + folders[i] + '/'
#print(folders)

# 5짜리 가중치 이미지 가져옴!

#video만 합치는 것
fps = 20
outpath = 'demo_video.mp4'

frames_to_video(folders,outpath,fps)

#audio만 빼내기
audiopath = 'audio_frames/audio006'

audio_list = os.listdir(audiopath)
audio_results = []

for audio in audio_list:
    temp = audio.split('.')[0].replace('audio','')
    #print(temp)
    if temp in lines2:
        audio_results.append(audio)
print(audio_results)


path = 'demo_audio/'
files = []
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for i,file in enumerate(files):
    if i == 0:
        result = AudioSegment.from_wav(path+file)
    else:
        result += AudioSegment.from_wav(path+file)

result.export('demo_audio.wav',format='wav')

# for audio in audio_results:
#     temp = audiopath+'/'+audio
#     shutil.copy2(temp, 'demo_audio/')
