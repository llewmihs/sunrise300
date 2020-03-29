from time import sleep, strftime, time # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today
from config import *    # my dropbox API key and Push bullet API key
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from picamera import PiCamera # raspberry pi camera
import progressbar
from glob import glob # for the file upload process
import sys


# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464) #use full resolution

def the_camera(no_of_frames, delay):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in progressbar.progressbar(range(no_of_frames)):
        file_path1 = "/home/pi/sunrise300/images/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        pic_time = strftime("%d-%B-%H-%M-%S") + ".JPG"
        file_path2 = "/home/pi/sunrise300/highRes/" + pic_time
        camera.capture(file_path1)
        sleep(0.2)
        camera.capture(file_path2)
        sleep(delay)
    camera.stop_preview()

def upload():
    glob_files = glob("/home/pi/sunrise300/highRes/*.JPG")
    for i in glob_files:
        with open(filename, "rb") as f:
            dbx.files_upload(f.read(), filename, mute = True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        the_camera(int(sys.argv[1]), int(sys.argv[2]))
    else:
        the_camera(900, 2)
    upload()

