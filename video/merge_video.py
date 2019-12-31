import cv2
import numpy as np
import os

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

fps = 20
inputpath = ['images/000001/','images/000002/','images/000004/','images/000005/',
             'images/000006/','images/000007/','images/000008/']
outpath = 'fv.mp4'

frames_to_video(inputpath,outpath,fps)