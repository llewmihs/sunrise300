# The sunrise4000 is a timelapsing Raspberry Pi which
# Gets the time of sunrise, and then creates a set of
# images which are uploaded to drop box
# Changes in this version:
# - to ease the load ont he Pi the cropping is done using PiCamera
#
#

# Module import starts here...
from picamera import PiCamera
from time import sleep, strftime 

from PIL import Image 
from glob import glob

from zipfile import ZipFile

# the Picamera
camera.resolution = (1640, 1232)

def the_camera(no_of_frames, delay):
    with picamera.PiCamera() as camera:
        camera.resolution = (1640, 1232)
        camera.start_preview()
        try:
            for i, filename in enumerate(camera.capture_continuous("/home/pi/sunrise300/images/" + 'IMAGE_{counter:04d}.jpg')):
                sleep(delay)
                if i == no_of_frames:
                    break
        finally:
            camera.stop_preview()

def the_cropper():
    # Setting the points for cropped image 
    left = 0
    upper = 0
    right = 1640
    lower = 923
    file_list = glob("/home/pi/sunrise300/images/*.jpg")
    for i in len(file_list):
        im = Image.open(file_list[i])
        im = im.crop((left, upper, right, lower))
        im.save(file_list[i])
