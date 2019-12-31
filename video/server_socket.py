import socket
import boto3
import botocore
import time

import argparse
import time
import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import subprocess
import torch.optim as optim
from torch.autograd import Variable
import os
import errno
import cv2
from torchvision import datasets, transforms
from classification.models import *
from pydub import AudioSegment
from PIL import Image
import random
import shutil
import main
import merge_subtitle


def divide_video(video_path):
    print('start divide_video')
    #download/demo.mp4
    vidcap = cv2.VideoCapture(video_path)
    temp = video_path.split('/')[1].split('.')[0]
    print(video_path)
    print(temp)
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:

            standard = sec/1 + 1
            path = 'data/video_process/%s/%06d/'%(temp,standard)
            image = cv2.resize(image,(448,448))
            image = cv2.transpose(image)
            image = cv2.flip(image, 1)

            try:
                if not(os.path.isdir(path)):
                    os.makedirs(os.path.join(path))
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            cv2.imwrite("data/video_process/%s/%06d/frame%06d.jpg"% (temp,standard,count), image)     # save frame as JPG file
        return hasFrames

    sec = 0
    frameRate = 0.05
    count = 0
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        success = getFrame(sec)

    return 'data/video_process/%s/'%temp

def video_to_audio(video_path):
    print('start video to audio')

    temp = video_path.split('/')[1].split('.')[0]
    command = "ffmpeg -i %s -ab 160k -ac 2 -ar 16000 -vn %s" % (video_path, 'download/'+temp+'.wav')
    subprocess.call(command, shell=True)

    return 'download/'+temp+'.wav'

def divide_audio(audio_path):
    temp = audio_path.split('/')[1].split('.')[0]
    sound = AudioSegment.from_wav(audio_path)
    seconds = len(sound)
    count = 1
    flag = True
    path = 'data/audio_process/%s/' % (temp)

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

        newsound.export('data/audio_process/%s/audio%06d.wav'%(temp,count), format='wav')
        count = count+1
    return 'data/audio_process/%s/'%(temp)

use_cuda = torch.cuda.is_available()
device = torch.device('cuda:0' if use_cuda else 'cpu')

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])

loader = transforms.Compose([transforms.ToTensor(), normalize])

def image_loader(frame_path):

    image = Image.open(frame_path)
    image = loader(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)
    return image.to(device)

def classify(model, path):

    model.eval()

    frames= []
    weights= []

    seconds_list = os.listdir(path)
    for second in seconds_list:
        path2 = path+second+'/'
        frame_list = os.listdir(path2)
        for frame in frame_list:
            path3 = path2+frame
            image = image_loader(path3)
            a = model(image)
            b = a.cpu().data.numpy()[0]
            b = list(b)
            b = b.index(max(b))+1

            frames.append(path3)
            weights.append(b)

    return frames, weights

class VGG(nn.Module):

    def __init__(self, features, num_classes=5, init_weights=True):
        super(VGG, self).__init__()
        self.features = features
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )
        if init_weights:
            self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


def make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


cfgs = {
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}


def _vgg(arch, cfg, batch_norm, pretrained, progress, **kwargs):
    if pretrained:
        kwargs['init_weights'] = False

    model = VGG(make_layers(cfgs[cfg], batch_norm=batch_norm), **kwargs)

    if pretrained:
        # state_dict = load_state_dict_from_url(, progress=progress)
        model.load_state_dict(torch.load(model_urls[arch]))
    return model


def vgg11(pretrained=False, progress=True, **kwargs):
    print('aa')
    return _vgg('vgg11', 'A', False, pretrained, progress, **kwargs)

#모델 불러오는 코드
modelpath = 'classification/models/vlog_001.pth'
model = vgg11()
model.load_state_dict(torch.load(modelpath))
model.to(device)

__aws_access_key_id__ = 'AKIAUVU7GVM2BBAVYU7J'
__aws_secret_access_key__ = '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'

s3 = boto3.client(
    's3',
    aws_access_key_id = __aws_access_key_id__,
    aws_secret_access_key = __aws_secret_access_key__)

demofilename = 'vlog_demo.mp4'
bucket_name = 'khu-thon'

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind(('',8080))
serverSock.listen(1)

print('aaaaaa')
while True:
    connectionSock, addr = serverSock.accept()
    print(str(addr), '에서 접속이 확인.')

    data = connectionSock.recv(1024)
    print('받은 데이터: ', data.decode('utf-8'))

    new_filename = ''
    #받은 데이터!
    #demo.mp4*0만

    if data.decode('utf-8').split('*')[0] == 'demo.mp4':
        time.sleep(15)
        new_filename = 'demo_success.mp4'
        s3.upload_file(demofilename, bucket_name, new_filename)
    else:
        time.sleep(15)
        #여기는 모르는
        #demo.mp4 -> demo
        weight = data.decode('utf-8').split('*')[1]
        s3name = data.decode('utf-8').split('*')[0]
        tempname = s3name.split('.')[0]
        print(s3name)
        s3.download_file(bucket_name, s3name, 'download/'+s3name)
        loadfile = 'download/'+s3name
        video_data_path = divide_video(loadfile)
        temp_audio_path = video_to_audio(loadfile)
        audio_data_path = divide_audio(temp_audio_path)

        # 모델 시작
        frame_list, weight_list = classify(model, video_data_path)

        # 으로 나누기
        length = int(len(weight_list)/20)
        num_list = []
        for i in range(0,int(length/2)):
            while True:
                num = random.randrange(1,length+1)
                if num not in num_list:
                    num_list.append(num)
                    break
        print(num_list)

        new_frame_list = []
        new_weight_list = []
        new_audio_list = []
        print(audio_data_path)
        for num in num_list:
            new_frame_list += frame_list[(num-1)*20:num*20]
            new_weight_list += weight_list[(num-1)*20:num*20]

        audio_list_temp = os.listdir(audio_data_path)
        for num in num_list:
            new_audio_list.append(audio_data_path+audio_list_temp[num-1])

        print(new_frame_list)
        print(new_weight_list)
        print(new_audio_list)

        new_frame_list.sort()
        new_audio_list.sort()
        #audio copy
        for audio in new_audio_list:
            shutil.copy2(audio, 'data/audio_copy')

        #frame 병합
        outputpath = 'data/video_merge/'+tempname+'.mp4'

        image_arr = []
        fps = 20
        for frame in new_frame_list:
            img = cv2.imread(frame)
            size =  (img.shape[1],img.shape[0])
            img = cv2.resize(img,size)
            image_arr.append(img)

        fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(outputpath,fourcc, fps, size)
        for i in range(len(image_arr)):
            out.write(image_arr[i])
        out.release()

        #audio 병합
        for i,file in enumerate(new_audio_list):
            if i == 0:
                result = AudioSegment.from_wav(file)
            else:
                result += AudioSegment.from_wav(file)
        outputpath2 = 'data/audio_merge/'+tempname+'.wav'
        result.export(outputpath2,format='wav')

        #두개 병합
        command = "ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s" % (outputpath,outputpath2, 'data/merge/'+tempname+'.mp4')
        subprocess.call(command, shell=True)

        #자막 만들기
        main.make_subtitle('data/audio_copy/')

        #자막 합치기
        new_filename = s3name + '_success.mp4'
        merge_subtitle.merge_subtitle('data/merge/'+tempname+'.mp4', 'data/script/script.srt', new_filename)

        s3.upload_file(loadfile, bucket_name, new_filename)

    connectionSock.send((new_filename + '\n').encode('utf-8'))
    print('메세지 보냈음')
