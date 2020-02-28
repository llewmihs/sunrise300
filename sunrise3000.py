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

from glob import glob # for the file upload process
import subprocess # to run file cleanup after the upload

from crontab import CronTab     # so that we can write to the crontab at the end of each day `pip3 install python-crontab`
from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time

# import logging  #create a logfile for debug purposes https://www.geeksforgeeks.org/logging-in-python/

# now the initial set-up: Dropbox and Pushbullet
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout
from pushbullet import Pushbullet
pb = Pushbullet(PUSHBULLET)

# logging.basicConfig(filename='/home/pi/sunrise300/logfile/app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
# logger=logging.getLogger() 

# the Picamera
camera = PiCamera()
camera.resolution = (3280, 2464)

def lapse_details(real_time):
    real_time = 90 * 60 # 90 minutes * 60 seconds
    film_length = 30
    frame_rate = 15
    total_frames = film_length * frame_rate
    delay = real_time / total_frames
    logger.info(f"Timelapse delay = {delay}, total frames = {total_frames}")
    return 4, 2
    #return total_frames, delay

def the_camera(no_of_frames, delay):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in range(total_frames):
        #create timestamp filename
        file_path = "/home/pi/sunrise300/images/" + strftime("%Y%m%d-%H%M%S")+".jpg"
        camera.capture(file_path)
        sleep(delay)
    camera.stop_preview()

def dropbox_uploader():
    files = glob('/home/pi/sunrise300/images/*.jpg')
    try:
        for i in range(len(files)):
            with open(files[i], "rb") as f:
                dbx.files_upload(f.read(), "/" + files[i], mute = True)
        print("Successfully uploaded")
    except:
        print("Failure to upload files to Dropbox")

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
    my_cron.remove_all()    # clear current crontab
    
    # set the cron job to run in the background
    job = my_cron.new(command='nohup python3 /home/pi/sunrise300/sunrise300.py &')
    job.hour.on(timelapse_start.hour)
    job.minute.on(timelapse_start.minute)
    my_cron.write() #write the job to the crontab

def clean_up():
    subprocess.call("/home/pi/sunrise300/images/*.jpg", shell=True)

if __name__ == "__main__":
    total_frames, delay = lapse_details(60)
    try:
        the_camera(total_frames, delay)
    except:
        print("There was an error during the timelapse photography")
    
    dropbox_uploader()

    lapse_start_time = start_time()

    cron_update(lapse_start_time)


