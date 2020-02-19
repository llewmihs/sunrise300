import dropbox
import os
from config import *
from time import sleep
from picamera import PiCamera

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture('foo.jpg')
camera.stop_preview()

with open("foo.jpg", "rb") as f:
    dbx.files_upload(f.read(), '/foo.jpg', mute = True)

# getting the filename from the user
file_path = "foo.jpg"

# checking whether file exists or not
if os.path.exists(file_path):
    # removing the file using the os.remove() method
    os.remove(file_path)
else:
    # file not found message
    print("File not found in the directory")