from pydub import AudioSegment
import os

path = 'audios/'
files = []
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for i,file in enumerate(files):
    if i == 0:
        result = AudioSegment.from_wav(path+file)
    else:
        result += AudioSegment.from_wav(path+file)

result.export('fa.wav',format='wav')