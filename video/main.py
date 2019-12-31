import seperate_audio
import stt
import upload_files
import time
import os


def make_subtitle(path):
    # Seperating audio file each 10 seconds
    pathcount = seperate_audio.seperate_audio(path)

    # Uploading files to google cloud storage
    upload_files.upload_files('data/sep/')

    # Making one subtitles file for separating audio files
    print("Start making subtitles")
    scriptdir = 'data/script/'
    script = open(scriptdir + 'script.srt', 'w', encoding='UTF-8')
    totaltime = 0
    for i in range(1, pathcount+1):
        start = time.time()
        response = stt.transcribe_gcs("gs://2019-khuthon-ddingdong/sep/sep{}.wav".format(i))
        for result in response.results[::-1]:
            alternative = result.alternatives[0]
            script.write('{}\n00:0{}:{}0,000 --> 00:0{}:{}0,000\n'.format(i,
                                                                    (i - 1) // 6, (i - 1) % 6,
                                                                    i // 6, i % 6))
            script.write('{}'.format(result.alternatives[0].transcript)+"\n\n")

        end = time.time()
        totaltime += end - start
        print('epoch: {}/{}\texecuting time: {}\ttotal execution time: {}'.format(i, pathcount, end-start, totaltime))
    print("Finished!")
