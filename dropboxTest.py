import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

#set up the camera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# Camera warm-up time
sleep(2)


for i in range(10):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    # upload the file to dropbox
    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), "/" + file_path, mute = True)

    # remove the file once upload complete
    if os.path.exists(file_path):
        # removing the file using the os.remove() method
        os.remove(file_path)
    else:
        # file not found message
        print("File not found in the directory")
    sleep(5)

camera.stop_preview()