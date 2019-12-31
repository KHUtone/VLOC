import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import time

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        enable_automatic_punctuation=True,
        audio_channel_count=2)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=485)

    return response

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    '''
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
    '''


def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        enable_automatic_punctuation=True)
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    savedir = 'data/scripts/audio006_scripts/'
    script = open(savedir + 'script.srt', 'a')
    for i in range(1, 49):
        start = time.time()
        response = transcribe_gcs("gs://2019-khuthon-ddingdong/audio006_frac/fa{}.wav".format(i))
        for result in response.results:
            alternative = result.alternatives[0]
            script.write(u'{}\n00:0{}:{}0,000 --> 00:0{}:{}0,000\n'.format(i,
                                                                     (i - 1) // 6, (i - 1) % 6,
                                                                     i // 6, i % 6))
            script.write(u'{}'.format(result.alternatives[0].transcript)+"\n\n")

        end = time.time()
        print('executing time: {}'.format(end-start))
    print("completed")

    # transcribe_gcs("gs://2019-khuthon-ddingdong/test8.wav")
