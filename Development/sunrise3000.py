# The sunrise3000 is a timelapsing Raspberry Pi which
# Gets the time of sunrise, and then creates a set of
# images which are uploaded to drop box

# modules needed for the timelapse
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
from config import *    # my dropbox API key and Push bullet API key

from time import sleep, strftime, time # for the picamera and to name the files
from datetime import datetime, timedelta       # possbily not needed but used to get the sunrise for today
import os.path
import sys

from picamera import PiCamera # raspberry pi camera

import subprocess # to run file cleanup after the upload
from twython import Twython, TwythonError # pip3 install twython

from crontab import CronTab     # so that we can write to the crontab at the end of each day `pip3 install python-crontab`
from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time
from glob import glob # for the file upload process
import logging

import progressbar

import sys # for argv testing

from PIL import Image #python3 -m pip install Pillow, also need: sudo apt-get install libopenjp2-7, sudo apt install libtiff5

# now the initial set-up: Dropbox and Pushbullet
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout
from pushbullet import Pushbullet
pb = Pushbullet(PUSHBULLET)

log_filename = strftime("%d%B%H") + ".log"

logging.basicConfig(filename=log_filename,level=logging.DEBUG)

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
    print(f"Croppping files to new res: {right} by {lower}")
    print(".........................................................")
    print("")
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
    print(f"The camera took {(no_of_frames)} images.")
    print(f"The camera ENDED taking images at {end_time}")
    print(".........................................................")
    print("")

    camera.stop_preview()

def test_lapser():
    print("Filename:")
    video = input()
    print("Framerate:")
    frames = input()
    print("CRF (17-22):")
    crf = input()
    print("Preset (slow, veryslow):")
    preset = input()
    start_time = time()
    print(f"Attempting to compile video file - < {video} > - using FFMPEG")
    print(".........................................................")
    subprocess.call(f"ffmpeg -y -r {frames} -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset {preset} -crf {crf} {video}", shell=True)
    end_time = time()
    elapsed_time_secs = int(end_time - start_time)
    elapsed_time_mins  = int(elapsed_time_secs / 60)
    print(f"Programme executed in {elapsed_time_mins} minutes")

    if os.path.exists(video): # has the file been written, and is it of a decent size?
        print(f"SUCCESS - FFMPEG created the video file: {video}")
        file_in_mb = int(os.path.getsize(video)/((1024*1024)))
        print(f"Fileseize: ~ {file_in_mb} Mb")
        push = pb.push_note(f"FFMPEG Timelapse Successful: {video}", f"Fileseize: {file_in_mb} Mb")
    else:
        print(f"ERROR - FFMPEG failed to create the video file: {video}")
        print(f"Programme exiting early")
        sys.exit()
        push = pb.push_note("There was a failure with the FFMPEG lapse.", "Uh oh")

def the_lapser(vid_file, fps):
    video = vid_file
    frames = fps
    start_time = time()
    print(f"Attempting to compile video file - < {video} > - using FFMPEG")
    print(".........................................................")
    subprocess.call(f"ffmpeg -y -r {frames} -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {video}", shell=True)
    end_time = time()
    elapsed_time_secs = int(end_time - start_time)
    elapsed_time_mins  = int(elapsed_time_secs / 60)
    print(f"Programme executed in {elapsed_time_mins} minutes")

    if os.path.exists(video): # has the file been written, and is it of a decent size?
        print(f"SUCCESS - FFMPEG created the video file: {video}")
        file_in_mb = int(os.path.getsize(video)/((1024*1024)))
        print(f"Fileseize: ~ {file_in_mb} Mb")
        push = pb.push_note(f"FFMPEG Timelapse Successful: {video}", f"Fileseize: {file_in_mb} Mb")
    else:
        print(f"ERROR - FFMPEG failed to create the video file: {video}")
        print(f"Programme exiting early")
        sys.exit()
        push = pb.push_note("There was a failure with the FFMPEG lapse.", "Uh oh")

def new_lapser(vid_file, fps):
    # check if the file has been created, and if not run the ffmpeg subprocess
    counter = 0
    video = vid_file
    frames = fps
    start_time = time()
    while os.path.exists(vid_file) == False:
        counter = counter + 1
        start_time = time()
        logging.info(f"Video file not created yet - running FFMPEG iteration: {counter}")
        subprocess.call(f"ffmpeg -nostdin -y -r {frames} -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {video}", shell=True)
    end_time = time()
    elapsed_time_secs = int(end_time - start_time)
    elapsed_time_mins  = int(elapsed_time_secs / 60)
    fs = int(os.path.getsize(vid_file)/((1024*1024)))
    logging.info(f"Video file << {vid_file} >> created - time {elapsed_time_mins} - file size {fs}")


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
    print(".........................................................")
    print("")

def file_size(filename):
    file_in_mb = int(os.path.getsize(filename)/((1024*1024)))
    print(f"file size is {file_in_mb} mb")
    return file_in_mb

def dropbox_uploader(filename):
    logging.info(f"Sunrise3000 will now upload the mp4 time lapse: {filename} to Dropbox.")
    try:
        with open(filename, "rb") as f:
            print(f"Trying file {filename}")
            print(f"Uploading now ->    ", end='')
            dbx.files_upload(f.read(), filename, mute = True)
            logging.info("SUCCESS")
        push = pb.push_note("Dropbox Upload Successful", "Well done.")
    except:
        push = pb.push_note("There was a failure with the Dropbox Upload.", "Uh oh")
        logging.info("FAILED")
    print(".........................................................")
    print("")

def start_time():
    # set Astral location for Whitley Bay
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, -1.4513)
     # get tomorrow's sunrise time
    s = sun(city.observer, date=datetime.date(datetime.now())+timedelta(days=1))
    sunrise_time = s['sunrise']   
    # timelapse shoudl start 1 hour prior
    timelapse_start = sunrise_time - timedelta(minutes=60)
    return timelapse_start

def cron_update(timelapse_start):
    my_cron = CronTab(user='pi')
    my_cron.remove_all(comment='foo')
    #my_cron.remove_all()    # clear current crontab
    # set the cron job to run in the background
    job = my_cron.new(command='./sun_launcher.sh', comment='foo')
    job.hour.on(timelapse_start.hour)
    job.minute.on(timelapse_start.minute)
    my_cron.write() #write the job to the crontab

def clean_up():
    try:
        subprocess.call("rm -r /home/pi/sunrise300/images/*.JPG", shell=True)
        subprocess.call("rm -r /home/pi/sunrise300/*.mp4", shell=True)
        logging.info(f'Cleanup complete: .mp4 and .JPG files removed')
    except:
        logging.info(f'Cleanup failed')
        pass

if __name__ == "__main__":
    
    now = strftime("%d%B%H%M") # get the start time of the programme
    logging.info(f'Timelapse started at {now}')
    clean_up()
    video_file = now + ".mp4"
    print(video_file)

    if len(sys.argv) > 1:
        logging.info("MANUAL EXECUTION")
        real_time = int(sys.argv[1])
        fps = int(sys.argv[2])
    else:
        logging.info("AUTOMATIC EXECUTION")
        real_time = 120
        fps = 30
    logging.info(f" - Total timelapse duration is: {real_time} minutes.")
    logging.info(f" - Output framerate  is: {fps} fps.")        
    total_frames, delay = lapse_details(real_time, fps)
    logging.info(f"** Programme set to take {total_frames} images, with a {delay} second delay.**")
    logging.info(".........................................................")

    push = pb.push_note(f"A {real_time} minutes timelapse Has Started at {now}.", f"Total frames: {total_frames}. Delay: {delay}. FPS. {fps}")
 
    the_camera(total_frames, delay)

    the_cropper()
    video_file = now + ".mp4"

    try:
        new_lapser(video_file, fps)

        glob_file = glob("/home/pi/sunrise300/*.mp4")[0]

        dropbox_uploader(glob_file)
    
    finally:
        lapse_start_time = start_time()
        cron_update(lapse_start_time)
        dropbox_uploader(log_filename)



    