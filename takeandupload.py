# modules needed for the timelapse
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from config import *    # my dropbox API key and Push bullet API key
from picamera import PiCamera # raspberry pi camera
from time import sleep, strftime # for the picamera and to name the files

# now the initial set-up: Dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

# the Picamera
camera = PiCamera()
camera.resolution = (1640, 1232)

def take_a_picture():
    
    filename = "IMAGE_" + strftime("%Y%m%d-%H%M%S") + ".JPG"
    print(f"Taking photo {filename}")
    camera.start_preview()
    sleep(2) # Camera warm-up time
    camera.capture(filename)
    return filename

def upload_to_dropbox(file_path):
    print(f"Uploading photo {file_path}")
    with open(file_path, "rb") as f:
        print(f"Trying file {file_path}")
        dbx.files_upload(f.read(), "/"+file_path, mute = True)
    print("Successfully uploaded")

if __name__ == "__main__":
    new_file = take_a_picture()
    upload_to_dropbox(new_file)
   