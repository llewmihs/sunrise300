# to run in back ground nohup python3 manuallapse.py &

import subprocess
import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera
import sys

# mobile notification software
from notify_run import Notify
notify = Notify()

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

#set up the camera
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()

# Camera warm-up time
sleep(2)


print("How long do you want to capture (minutes)?")
real_time = int(input()) * 60
film_length = 30
frame_rate = 15

total_frames = film_length * frame_rate

delay = real_time / total_frames
print("The delay is %d seconds" % delay)

print("Taking images...")
notify.send("Taking %d frames with a %d second delay" % (total_frames, delay))
for i in range(total_frames):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    print(i)
    sleep(delay)
print("Stills complete.")
notify.send("Images complete")

vid_path = strftime("%Y%m%d-%H%M%S")+".mp4"

subprocess.call("ls *.jpg > stills.txt", shell=True)

print("Building video...")
#subprocess.call("mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o %s -mf type=jpeg:fps=15 mf://@stills.txt" % vid_path,shell=True)
subprocess.call("mencoder mf://*.jpg -nosound -of lavf -lavfopts format=mp4 -ovc x264 -x264encopts pass=1:bitrate=2000:crf=24 -o %s -mf type=jpg:fps=15" % vid_path,shell=True)


print("Uploading video...")
with open(vid_path, "rb") as f:
    dbx.files_upload(f.read(), "/" + vid_path, mute = True)


print("Cleaning up...")
subprocess.call("rm -r stills.txt", shell=True)
subprocess.call("rm -r *.avi", shell=True)
subprocess.call("rm -r *.jpg", shell=True)
print("Fin")
notify.send("Upload complete")