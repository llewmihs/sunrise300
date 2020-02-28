# module import
import dropbox      # for uploading to dropbox
from config import *    # my dropbox API key

# mobile notification software
from notify_run import Notify
notify = Notify()

from time import sleep, strftime    # for filenaming and time
from picamera import PiCamera       # the picamera

from datetime import datetime, timedelta    # for the current time and adding time
import pytz                         # to enale comparison of datetime and astral time, astral is ofset, datetime is naive
from astral import LocationInfo     # to get the location info
from astral.sun import sun          # to get the sunrise time

import subprocess       # to stitch the film into a timelapse

# initial setup
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout=None)        # dropbox, with Timeout so that avi uploads work

#set up the camera
camera = PiCamera()
camera.resolution = (1920, 1080)

#number of frames needed
vid_length = 60
fps = 15
frames_req = vid_length * fps
real_time = 60 * 60
time_delay = real_time / frames_req

# ofset setting
utc=pytz.UTC

# set Astral location for Whitley Bay
city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, 1.4513)

if __name__ == "__main__":
    while True:
        print("Checking the suntime, and now time")
        # get the current time
        now = utc.localize(datetime.now())
        print("Current time:")
        print(now)

        # get today's sunrise time
        s = sun(city.observer, date=datetime.date(datetime.now()))
        print("Today's sunrise is at:")
        print(s['sunrise'])

        sunrise_time = s['sunrise']

        # get the timelapse start time
        lapse_window_open = sunrise_time - timedelta(minutes=40)
        lapse_window_closed = sunrise_time - timedelta(minutes=20)

        # checking details
        before = utc.localize(datetime.now()) < lapse_window_open
        after = utc.localize(datetime.now()) > lapse_window_open

        print(before)
        print(after)

        # notify settings
        #notify.send("Before: %s, After: %s" % before, after)

        # now check if the timelapse window is open
        print("Timelapse will start at %s" % lapse_window_open)

        if lapse_window_open < utc.localize(datetime.now()) < lapse_window_closed:
            print("Timelapse time")
            notify.send("Timelapse has started")
            #start the camera
            camera.start_preview()
            # Camera warm-up time
            sleep(2)

            for i in range(900):
                #create timestamp filename
                file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
                # capture the files
                camera.capture(file_path)
                # wait for the next frame
                sleep(time_delay)
            
            print("Image capture complete")
            notify.send("Image capture complete")

            #start the camera
            camera.stop_preview()

            # now let's create the video
            vid_name = strftime("%Y%m%d")+".avi"
            subprocess.call("ls *.jpg > stills.txt", shell=True)
            subprocess.call("mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o %s -mf type=jpeg:fps=15 mf://@stills.txt" % vid_name ,shell=True)
            
            subprocess.call("rm -r *.jpg", shell=True)

            with open(vid_name, "rb") as f:
                dbx.files_upload(f.read(), "/" + vid_name, mute = True)

            subprocess.call("rm -r stills.txt", shell=True)
            subprocess.call("rm -r %s" % vid_name, shell=True)
        
        # wait 5 minutes
        sleep(300)