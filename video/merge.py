import subprocess
command = "ffmpeg -i demo_video.mp4 -i demo_audio.wav -c:v copy -c:a aac -strict experimental demo_final.mp4"
subprocess.call(command, shell=True)
