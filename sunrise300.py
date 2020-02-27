# import the necessary modules
import dropbox      # for uploading to dropbox
from config import *    # my dropbox API key and Push bullet API key

from time import sleep, strftime # for the picamera and to name the files
from picamera import PiCamera

from glob import glob # for the file upload process
import subprocess # to run file cleanup after the upload

from crontab import CronTab     # so that we can write to the crontab at the end of each day
from astral import LocationInfo     # to get the location info
from astral.sun import sun          # to get the sunrise time
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

# set up notification software
from pushbullet import Pushbullet
pb = Pushbullet(PUSHBULLET)

#set up the camera
camera = PiCamera()
camera.resolution = (3280, 2464)
camera.start_preview()
sleep(2) # Camera warm-up time

# calculate the lapse
real_time = 90 * 60 # 90 minutes * 60 seconds
film_length = 30
frame_rate = 15
#total_frames = film_length * frame_rate
total_frames = 10
delay = real_time / total_frames

push = pb.push_note("The Timelapse Has Started", "The delay is %d seconds" % delay)

for i in range(total_frames):
    #create timestamp filename
    file_path = strftime("%Y%m%d-%H%M%S")+".jpg"
    camera.capture(file_path)
    print(i)
    sleep(delay)
camera.stop_preview()

push = pb.push_note("Timelapse complete", "Upload begins")

files = glob('*.jpg')
for i in range(len(files)):
    with open(files[i], "rb") as f:
        dbx.files_upload(f.read(), "/" + files[i], mute = True)

push = pb.push_note("Job done", "Upload complete")


try:
        # now set the next time this programme runs
    my_cron = CronTab(user='pi')

    # set Astral location for Whitley Bay
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, -1.4513)

    # get today's sunrise time
    s = sun(city.observer, date=datetime.date(datetime.now()))
    sunrise_time = s['sunrise']

    # timelapse shoudl start 1 hour prior
    timelapse_start = sunrise_time - timedelta(minutes=60)

    # clear current crontab
    my_cron.remove_all()

    # set the cron job to run in the background
    job = my_cron.new(command='nohup python3 /home/pi/sunrise300.py &', comment=datetime.now())
    job.hour.on(timelapse_start.hour)
    job.minute.on(timelapse_start.minute)

    #write the job to the crontab
    my_cron.write()

    for job in my_cron:
        push = pb.push_note("New crontab installed", job)
except:
    push = pb.push_note("New crontab failed")



