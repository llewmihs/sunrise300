# to run in back ground nohup python3 justpics.py &
import subprocess
import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera
import sys
from glob import glob

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

from pushbullet import Pushbullet
pb = Pushbullet(PUSHBULLET)

push = pb.push_note("This is the title", "This is the body")

#set up the camera
camera = PiCamera()

camera.resolution = (3280, 2464)
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

print("Taking images...")
for i in range(total_frames):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    print(i)
    sleep(delay)

camera.stop_preview()

files = glob('*.jpg')

for i in range(len(files)):
    with open(files[i], "rb") as f:
        dbx.files_upload(f.read(), "/" + files[i], mute = True)
