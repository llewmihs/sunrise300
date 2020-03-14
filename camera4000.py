from time import sleep, strftime, time # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today

from picamera import PiCamera # raspberry pi camera
import progressbar

from PIL import Image #python3 -m pip install Pillow, also need: sudo apt-get install libopenjp2-7, sudo apt install libtiff5

# the Picamera
camera = PiCamera()
camera.resolution = (1640, 1232)

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
    for i in progressbar.progressbar(range(no_of_frames)):
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
    print("Calcuating timelapse details")
    total, delay = lapse_details(90, 30)
    print("Taking images")
    the_camera(total, delay)
    print("Finished")