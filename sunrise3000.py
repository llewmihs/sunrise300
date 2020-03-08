# The sunrise3000 is a timelapsing Raspberry Pi which
# Gets the time of sunrise, and then creates a set of
# images which are uploaded to drop box

# modules needed for the timelapse
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
from config import *    # my dropbox API key and Push bullet API key

from time import sleep, strftime # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today
import os.path

from picamera import PiCamera # raspberry pi camera

import subprocess # to run file cleanup after the upload
from twython import Twython, TwythonError # pip3 install twython

from crontab import CronTab     # so that we can write to the crontab at the end of each day `pip3 install python-crontab`
from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time
from glob import glob # for the file upload process

import progressbar

# saveout = sys.stdout   
# logfile = strftime("%d %B - %H %M") + ".log"                              
# fsock = open(logfile, 'w') 
# sys.stdout = fsock 

import sys # for argv testing

from PIL import Image #python3 -m pip install Pillow, also need: sudo apt-get install libopenjp2-7, sudo apt install libtiff5

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

def the_cropper():
    # Setting the points for cropped image 
    left = 0
    upper = 0
    right = 1640
    lower = 922
    file_list = glob("/home/pi/sunrise300/images/*.JPG")
    for names in progressbar.progressbar(file_list):
        im = Image.open(names)
        im = im.crop((left, upper, right, lower))
        im.save(names)

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
    print(f"The camera took {len(no_of_frames)} images.")
    print(f"The camera ENDED taking images at {end_time}")
    print(".........................................................")
    print("")

    camera.stop_preview()

def the_lapser(vid_file, fps):
    video = vid_file
    frames = fps
    print(f"Attempting to compile video file - < {video} > - using FFMPEG")
    print("***************************************************************")
    print("")
    
    subprocess.run(f"ffmpeg -y -r {frames} -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset veryslow -crf 17 {video}", capture_output=True, shell=True)

    if os.path.exists(video) and os.path.getsize(video) > 4000000: # has the file been written, and is it of a decent size?
        print(f"SUCCESS - FFMPEG created the video file: {video}")
        file_in_mb = os.path.getsize(video)/((1024*1024))
        print(f"Fileseize: {file_in_mb} Mb")
        push = pb.push_note(f"FFMPEG Timelapse Successful: {video}", f"Fileseize: {file_in_mb} Mb")
    else:
        print(f"ERROR - FFMPEG failed to create the video file: {video}")
        print(f"Programme exiting early")
        sys.exit()
        push = pb.push_note("There was a failure with the FFMPEG lapse.", "Uh oh")

def upload_to_twitter(vid_file):
    print("Twython will now upload the mp4 time lapse to Twitter.")
    try:
        print(f"Opening the video file -> {vid_file}    ", end = '')
        video = open(f'{vid_file}', 'rb')
        print("Success")
        print("Getting response from Twitter using credentials ->   ", end = '')
        response = twitter.upload_video(media=video, media_type='video/mp4')
        print("Success")
        print("Uploading Tweet ->   ", end = '')
        twitter.update_status(status="Here's this morning's sunrise...", media_ids=[response['media_id']])
        print("Success")
    except TwythonError as e:
        print("There was an error...")
        print(e)
        push = pb.push_note("There was a failure with the Twitter Upload.", e)
    print("***************************************************************")
    print("")

def dropbox_uploader(filename):
    print(f"Twython will now upload the mp4 time lapse: {filename} to Dropbox.")
    try:
        with open(filename, "rb") as f:
            print(f"Trying file {filename}")
            print(f"Uploading now ->    ", end='')
            dbx.files_upload(f.read(), filename, mute = True)
            print("SUCCESS")
        push = pb.push_note("Dropbox Upload Successful", "Well done.")
    except:
        push = pb.push_note("There was a failure with the Dropbox Upload.", "Uh oh")
        print("FAILED")

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
    try:
        subprocess.call("rm -r /home/pi/sunrise300/images/*.JPG", shell=True)
        subprocess.call("rm -r /home/pi/sunrise300/*.mp4", shell=True)
    except:
        pass

if __name__ == "__main__":

    clean_up()
    
    now = strftime("%Y %B %d - %H %M %S") # get the start time of the programme
    print("------------------ Timelapse 3000 Logfile ------------------ ")
    print("Runtime: " + now )
    print(".........................................................")
    print("")

    if len(sys.argv) > 1:
        print("MANUAL EXECUTION")
        real_time = int(sys.argv[1])
        fps = int(sys.argv[2])
    else:
        print("AUTOMATIC EXECUTION")
        real_time = 60
        fps = 15
    print(f" - Total timelapse duration is: {real_time} minutes.")
    print(f" - Output framerate  is: {fps} fps.")        
    total_frames, delay = lapse_details(real_time, fps)
    print(f"** Programme set to take {total_frames} images, with a {delay} second delay.**")
    print(".........................................................")
    print("")
    push = pb.push_note(f"A {real_time} minutes timelapse Has Started at {now}.", f"Total frames: {total_frames}. Delay: {delay}. FPS. {fps}")
 
    the_camera(total_frames, delay)

    
    try:
        the_lapser(vid_file, fps)

        glob_file = glob("/home/pi/sunrise300/*.mp4")[0]

        dropbox_uploader(glob_file)
    
        # if len(sys.argv) > 1:
        #     print("Test run, not uploading")
        # else:
        #     upload_to_twitter(glob_file)
    finally:
        lapse_start_time = start_time()
        cron_update(lapse_start_time)
        # sys.stdout = saveout                                     6
        # fsock.close()


    