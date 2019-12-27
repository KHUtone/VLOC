import os
import shutil

video_list = os.listdir('videos/')

print(video_list) #비디오 폴더 리스트

for video_number in video_list:
    #video_number = video001 형식
    f = open("labels\\" + video_number + ".txt", 'r')

    #video001의 초당 폴더들(000001, 000002, ...)
    video_folder_list = os.listdir("videos\\"+video_number)
    print("video_folder_list : {}".format(video_folder_list)) #

    #0000001, 000002, 000003, ...
    for folder_number in video_folder_list:

        #000001, 000002, 000003 ...의 frame들 (frame000001.jpg, frame000002.jpg ...)
        frame_list = os.listdir("videos\\" + video_number + "\\"+folder_number)
        #print("frame_list : {}".format(frame_list))

        # video 초당 폴더들 및 가중치(000001 4, 000002 4, 000003 5 ...)
        weight_value = f.readline()
        #print(weight_value)

        if(video_number == "video006"):
            if (weight_value[6:8] == " 1"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\test\\1\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 2"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\test\\2\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 3"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\test\\3\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 4"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\test\\4\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 5"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\test\\5\\" + video_number + "_" + folder_number + "_" + frame_number)

        else:
            if(weight_value[6:8] == " 1"):
                for frame_number in frame_list:
                                # videos\video001\000001\frame000000.jpg
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                # data\train\1\video001_000001_frame000000.jpg
                                "data\\train\\1\\" + video_number+"_"+folder_number + "_" + frame_number)
            elif(weight_value[6:8] == " 2"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\train\\2\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 3"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\train\\3\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 4"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\train\\4\\" + video_number + "_" + folder_number + "_" + frame_number)
            elif (weight_value[6:8] == " 5"):
                for frame_number in frame_list:
                    shutil.copy("videos\\" + video_number + "\\" + folder_number + "\\" + frame_number,
                                "data\\train\\5\\" + video_number + "_" + folder_number + "_" + frame_number)

    print("{} 폴더 작업 완료".format(video_number))


