from pydub import AudioSegment
import os

def seperate_audio(path):
    print("Start seperating audio files...")
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    pathcount = len(files)
    savedir = 'data/sep/'
    segment = 10
    for i,file in enumerate(files):
        final = i
        if i == 0:
            result = AudioSegment.from_wav(path + file)
        if i % 10 == 0 and i != 0:
            result.export(savedir + 'sep{}.wav'.format(i // 10), format='wav')
            result = AudioSegment.from_wav(path+file)
        else:
            result += AudioSegment.from_wav(path+file)

    result.export(savedir + 'sep{}.wav'.format(final // 10),format='wav')
    print("Finished!")

    print(pathcount)
    return pathcount // 10
