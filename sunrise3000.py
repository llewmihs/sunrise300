# The sunrise3000 is a timelapsing Raspberry Pi which
# Gets the time of sunrise, and then creates a set of
# images which are uploaded to drop box

# modules needed for the timelapse
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
from config import *    # my dropbox API key and Push bullet API key

from time import sleep, strftime # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today

from picamera import PiCamera # raspberry pi camera

import subprocess # to run file cleanup after the upload
from twython import Twython # pip3 install twython

from crontab import CronTab     # so that we can write to the crontab at the end of each day `pip3 install python-crontab`
from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time
from glob import glob # for the file upload process

import progressbar

import sys # for argv testing

# now the initial set-up: Dropbox and Pushbullet
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout
from pushbullet import Pushbullet
pb = Pushbullet(PUSHBULLET)

now = strftime("%Y%m%d")

vid_file = "/home/pi/sunrise300/" + strftime("%Y%m%d-%H%M") + ".mp4"

# the Picamera
camera = PiCamera()
camera.resolution = (1640, 1232)

# Twython setup
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def lapse_details(duration_in_minutes):
    real_time = duration_in_minutes * 60 # minutes * 60 seconds
    film_length = 30
    frame_rate = 15
    total_frames = film_length * frame_rate
    delay = real_time / total_frames
    return total_frames, delay

def the_camera(no_of_frames, delay):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in progressbar.progressbar(range(no_of_frames)):
        #create timestamp filename
        file_path = "/home/pi/sunrise300/images/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)

        sleep(delay)
    camera.stop_preview()

def the_lapser(vid_file):
    video = vid_file
    try:
        subprocess.call(f"ffmpeg -y -r 15 -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vf crop=1640:923:0:0 -vcodec libx264 -preset veryslow -crf 17 {video}", shell=True)
        push = pb.push_note("FFMPEG Timelapse Successful", "Well done.")
    except:
        push = pb.push_note("There was a failure with the FFMPEG lapse.", "Uh oh")

def upload_to_twitter(vid_file):
    try:
        video = open(f'{vid_file}', 'rb')
        response = twitter.upload_video(media=video, media_type='video/mp4')
        twitter.update_status(status="Here's this morning's sunrise...", media_ids=[response['media_id']])
    except:
        push = pb.push_note("There was a failure with the Twitter Upload.", "Uh oh")

def dropbox_uploader(filename):
    try:
        with open(filename, "rb") as f:
            print(f"Trying file {filename}")
            dbx.files_upload(f.read(), filename, mute = True)
        push = pb.push_note("Dropbox Upload Successful", "Well done.")
    except:
        push = pb.push_note("There was a failure with the Dropbox Upload.", "Uh oh")

def start_time():
    # set Astral location for Whitley Bay
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, -1.4513)
     # get tomorrow's sunrise time
    s = sun(city.observer, date=datetime.date(datetime.now())+timedelta(days=1))
    sunrise_time = s['sunrise']   
    # timelapse shoudl start 1 hour prior
    timelapse_start = sunrise_time - timedelta(minutes=40)
    return timelapse_start

def cron_update(timelapse_start):
    my_cron = CronTab(user='pi')
    my_cron.remove_all(comment='foo')
    #my_cron.remove_all()    # clear current crontab
    # set the cron job to run in the background
    job = my_cron.new(command='nohup python3 /home/pi/sunrise300/sunrise3000.py &', comment='foo')
    job.hour.on(timelapse_start.hour)
    job.minute.on(timelapse_start.minute)
    my_cron.write() #write the job to the crontab

def clean_up():
    subprocess.call("rm -r /home/pi/sunrise300/images/*.JPG", shell=True)
    subprocess.call("rm -r /home/pi/sunrise300/*.mp4", shell=True)

if __name__ == "__main__":
    
    clean_up()
    
    now = strftime("%Y%m%d-%H%M%S") # get the start time of the programme

    if len(sys.argv) > 1:
        print("Args")
        total_frames = lapse_details(int(sys.argv[1]))
        delay = lapse_details(int(sys.argv[2]))
        push = pb.push_note(f"A FALSE Timelapse Has Started at {now}.", "This is running as a test.")
    else:
        print("No args")
        total_frames, delay = lapse_details(60)
        push = pb.push_note(f"A TRUE Timelapse Has Started at {now}.", "Happy lapsing.")
 
    the_camera(total_frames, delay)

    
    try:
        the_lapser(vid_file)

        glob_file = glob("/home/pi/sunrise300/*.mp4")[0]

        dropbox_uploader(glob_file)
    
        # if len(sys.argv) > 1:
        #     print("Test run, not uploading")
        # else:
        #     upload_to_twitter(glob_file)
    finally:
        lapse_start_time = start_time()
        cron_update(lapse_start_time)


    