from time import sleep, strftime, time
from picamera import PiCamera
from config import *
import dropbox

#dropbox, timeout=none allows for uploading of larger files without 30second normal timeout
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) 

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

def take_a_picture():
    print("Taking a photo")
    camera.start_preview()
    sleep(2)
    file_path = "/home/pi/sunrise300/images/" + strftime("%H-%M-%S") + ".JPG"
    camera.capture(file_path)
    camera.stop_preview()
    return file_path

def  upload_to_dropbox(filepath):
    print("Uploading to Dropbox")
    with open(filepath, "rb") as f:
        dbx.files_upload(f.read(), filepath, mute = True)

if __name__ == "__main__":
    upload_to_dropbox(take_a_picture())