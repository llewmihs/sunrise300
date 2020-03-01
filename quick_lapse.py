
# modules needed for the timelapse
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from config import *    # my dropbox API key and Push bullet API key
from time import sleep, strftime # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today
from picamera import PiCamera # raspberry pi camera
import subprocess # to run file cleanup after the upload
from glob import glob # for the file upload process

# the Picamera
camera = PiCamera()
camera.resolution = (1640, 1232)

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

def lapse_details(real_time):
    real_time = 90 * 60 # 90 minutes * 60 seconds
    film_length = 30
    frame_rate = 15
    total_frames = film_length * frame_rate
    delay = real_time / total_frames
    #return 1, 2
    return total_frames, delay

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

if __name__ == "__main__":
    the_camera(45,1)

    subprocess.call("ffmpeg -r 15 -f image2 -start_number 0000 -i /home/pi/sunrise300/minilapse/IMAGE_%04d.JPG -vf crop=1640:923:0:0 -codec:v prores -profile:v 2 /home/pi/sunrise300/minilapse/preview.mov", shell=True)

    dropbox_uploader()



