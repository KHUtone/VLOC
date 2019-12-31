import subprocess
command = "ffmpeg -i fv.mp4 -i audio006.wav -c:v copy -c:a aac -strict experimental final.mp4"
subprocess.call(command, shell=True)