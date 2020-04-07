from time import sleep, strftime, time
from picamera import PiCamera
from config import *
import dropbox

#dropbox, timeout=none allows for uploading of larger files without 30second normal timeout
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) 

# the Picamera, at full resolution
camera = PiCamera()
camera.resolution = (3280, 2464)

def take_a_picture():
    print("Taking a photo")
    camera.start_preview()
    sleep(2)
    file_name = strftime("%H-%M-%S") + ".JPG"
    full_path = "/home/pi/sunrise300/images/" + file_name
    camera.capture(full_path)
    camera.stop_preview()
    return full_path, file_name

def  upload_to_dropbox(filepath, filename):
    print("Uploading to Dropbox")
    dropbox_filepath = "/SunriseImages/"+filename
    with open(filepath, "rb") as f:
        dbx.files_upload(f.read(), dropbox_filepath, mute = True)

if __name__ == "__main__":
    i, j = take_a_picture()
    upload_to_dropbox(i,j)