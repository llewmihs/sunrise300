# to run in back ground nohup python3 justpics.py &


import subprocess
import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera
import sys
from glob import glob

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

# print("How long do you want to capture (minutes)?")
# real_time = int(input()) * 60
real_time = 60 * 60
film_length = 30
frame_rate = 15

total_frames = film_length * frame_rate

delay = real_time / total_frames

print("The delay is %d seconds" % delay)

notify.send("Starting to take pictures")

print("Taking images...")
for i in range(total_frames):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    print(i)
    sleep(delay)

camera.stop_preview()

notify.send("Starting to take upload")

files = glob('*.jpg')

for i in range(len(files)):
    with open(files[i], "rb") as f:
        dbx.files_upload(f.read(), "/" + files[i], mute = True)

notify.send("Upload complete")