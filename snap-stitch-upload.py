from time import sleep, strftime
from picamera import PiCamera

import cv2
import numpy as np
import glob
import dropbox
from config import *

#set up the camera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# Camera warm-up time
sleep(2)

for i in range(50):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    print(i)
    sleep(1)

# stitch
img_array = []
for filename in glob.glob('*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
out = cv2.VideoWriter('project1.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

print("Stitch complete")
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

# upload
# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

with open('project1.avi', "rb") as f:
    dbx.files_upload(f.read(), "/project1.avi", mute = True)

print("Upload complete")