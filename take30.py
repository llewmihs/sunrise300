# this test programme takes 30 photos and saves them to a folder
from picamera import PiCamera # raspberry pi cameraexit
from config import *
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
import subprocess
from glob import glob # for the file upload process
from time import sleep, strftime

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

def dropbox_uploader(file_path):
    files = file_path
    print(files)

    with open(files, "rb") as f:
        print(f"Tring file {files}")
        dbx.files_upload(f.read(), files, mute = True)
        print("Successfully uploaded")

if __name__ == "__main__":
    the_camera(45,0.5)
    vid_file = "/home/pi/sunrise300/minilapse/" + strftime("%Y%m%d-%H%M")+".mp4"
    subprocess.call(f"ffmpeg -y -r 15 -f image2 -start_number 0000 -i /home/pi/sunrise300/minilapse/IMAGE_%04d.JPG -vf crop=1640:923:0:0 -vcodec libx264 -pix_fmt yuv420p {vid_file}", shell=True)
    dropbox_uploader(vid_file)