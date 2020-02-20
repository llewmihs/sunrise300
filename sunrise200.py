#import the necessary modules
import subprocess
import dropbox
import os
from config import *
from time import sleep, strftime
from picamera import PiCamera
from astral import LocationInfo
import datetime

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

#set up the camera
camera = PiCamera()
camera.resolution = (1920, 1080)

#get location info
city = LocationInfo("Newcastle Upon Tyne", "England", "Europe/London", 55.0464, 1.4513)

# get today's date

# get today's sunrise time

# compare current time to sunrise time
