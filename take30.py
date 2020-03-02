# this test programme takes 30 photos and saves them to a folder
from picamera import PiCamera # raspberry pi cameraexit
from config import *
import dropbox      # for uploading to dropbox, `pip3 install dropbox`

# the Picamera
camera = PiCamera()
camera.resolution = (1640, 1232)

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

def the_camera(no_of_frames, delay):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(no_of_frames):
        #create timestamp filename
        print(f'Taking photo {i} of {no_of_frames}')
        file_path = "/home/pi/sunrise300/minilapse/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)
        sleep(delay)
    camera.stop_preview()

def dropbox_uploader():
    files = glob('/home/pi/sunrise300/minilapse/*.mov')
    print(files)
    for i in range(len(files)):
        with open(files[i], "rb") as f:
            print(f"Tring file {files[i]}")
            dbx.files_upload(f.read(), files[i], mute = True)
        print("Successfully uploaded")