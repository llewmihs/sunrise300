import dropbox
from config import *
from time import sleep, strftime
from picamera import PiCamera

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

#set up the camera
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()

# Camera warm-up time
sleep(2)

#create timestamp filename
file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
camera.capture(file_path)
camera.stop_preview()

with open(file_path, "rb") as f:
    dbx.files_upload(f.read(), "/" + file_path, mute = True)
print("Image %s uploaded." % file_path)