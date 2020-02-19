import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

file_path = strftime("%Y%m%d-%H%M%S")+".jpg"

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(file_path)
camera.stop_preview()

with open(file_path, "rb") as f:
    dbx.files_upload(f.read(), file_path, mute = True)

# # getting the filename from the user
# file_path = "foo.jpg"

# # checking whether file exists or not
# if os.path.exists(file_path):
#     # removing the file using the os.remove() method
#     os.remove(file_path)
# else:
#     # file not found message
#     print("File not found in the directory")