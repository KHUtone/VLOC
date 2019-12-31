import cv2
import os
import errno

video_list = []
video_list = os.listdir('videos/')

# hard code
#video_list = ['video001.mp4']
video_list.remove('video001.mp4')
video_list.remove('video002.mp4')
video_list.remove('video007.mp4')
video_list.remove('video008.mp4')
video_list.remove('video009.mp4')
video_list.remove('video010.mp4')

for video in video_list:
    video_path = 'videos/'+video
    vidcap = cv2.VideoCapture(video_path)
    temp = video.split('.')[0]
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:

            standard = sec/1 + 1
            path = 'frames/%s/%06d/'%(temp,standard)
            image = cv2.resize(image,(448,448))
            image = cv2.transpose(image)
            image = cv2.flip(image, 1)

            try:
                if not(os.path.isdir(path)):
                    os.makedirs(os.path.join(path))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            cv2.imwrite("frames/%s/%06d/frame%06d.jpg"% (temp,standard,count), image)     # save frame as JPG file
        return hasFrames

    sec = 0
    frameRate = 0.05
    count = 0
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        success = getFrame(sec)
