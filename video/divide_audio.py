from pydub import AudioSegment
import os
import errno

audio_list = []
audio_list = os.listdir('audios/')

for audio in audio_list:
    audio_path = 'audios/'+audio
    temp = audio.split('.')[0]
    sound = AudioSegment.from_wav(audio_path)

    # seconds = len(sound)/1000
    # count = 1
    # while True:
    #     newsound = sound[1000*(count-1):1000*count]
    #     newsound.export('audio1/audio_%05d.mp3' % count, format='mp3')
    #     count +=1
    #     if count > seconds:
    #         break

    # newsound = sound[:477000]
    # newsound.export('temp.wav', format='wav')

    seconds = len(sound)
    count = 1
    flag = True
    path = 'audio_frames/%s/' % (temp)

    while flag:
        if seconds - 1000*(count-1) <1000:
            newsound = sound[1000*(count-1):]
            flag=False
        else:
            newsound = sound[1000*(count-1):1000*count]

        try:
            if not(os.path.isdir(path)):
                os.makedirs(os.path.join(path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        newsound.export('audio_frames/%s/audio%06d.wav'%(temp,count), format='wav')
        count = count+1
