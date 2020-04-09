from time import sleep, strftime, time # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today
from config import *    # my dropbox API key and Push bullet API key

from picamera import PiCamera # raspberry pi camera

import sys

from PIL import Image #python3 -m pip install Pillow, also need: sudo apt-get install libopenjp2-7, sudo apt install libtiff5

from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

def lapse_details(duration_in_minutes, fps):
    print(f"User lapse duration request: {duration_in_minutes} minutes.")
    real_time = duration_in_minutes * 60 # minutes * 60 seconds
    film_length = 30
    frame_rate = fps
    total_frames = film_length * frame_rate
    delay = real_time / total_frames
    return total_frames, delay

def the_camera(no_of_frames, delay):
    start_time = strftime("%H:%M:%S")
    print(f"The camera BEGAN taking images at {start_time}")
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(no_of_frames):
        #create timestamp filename
        file_path = "/home/pi/sunrise300/images/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)
        sleep(delay)
    end_time = strftime("%H:%M:%S")
    print(f"The camera took {(no_of_frames)} images.")
    print(f"The camera ENDED taking images at {end_time}")
    print(".........................................................")
    print("")
    camera.stop_preview()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        duration = int(sys.argv[1])
    else:
        duration = 90
    total, delay = lapse_details(duration, 30)
    push = pb.push_note("A timelapse Has Started", f"Total frames: {total}. Delay: {delay}. FPS. 30")
    the_camera(total, delay)
    
