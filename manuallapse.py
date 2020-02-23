import subprocess
import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera
import sys

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

#set up the camera
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()

# Camera warm-up time
sleep(2)
print("How many images do you want to take?")
no_of_pics = input()

print("Taking images...")
for i in range(no_of_pics):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    print(i)
    sleep(2)
print("Stills complete.")

vid_path = strftime("%Y%m%d-%H%M%S")+".avi"

subprocess.call("ls *.jpg > stills.txt", shell=True)

print("Building video...")
subprocess.call("mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o %s -mf type=jpeg:fps=15 mf://@stills.txt" % vid_path,shell=True)



print("Uploading video...")
with open(vid_path, "rb") as f:
    dbx.files_upload(f.read(), "/" + vid_path, mute = True)


print("Cleaning up...")
subprocess.call("rm -r stills.txt", shell=True)
subprocess.call("rm -r *.avi", shell=True)
subprocess.call("rm -r *.jpg", shell=True)
print("Fin")