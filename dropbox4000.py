import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from config import *    # my dropbox API key and Push bullet API key
import subprocess # to run file cleanup after the upload
from glob import glob # for the file upload process
from time import sleep, strftime, time # for the picamera and to name the files
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)
import sys

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

def rename():
    if len(sys.argv) > 1:
        new_file = glob("/home/pi/sunrise300/*.mp4")[0]
    else:
        old_file_a = "/home/pi/sunrise300/timelapse-a.mp4"
        old_file_b = "/home/pi/sunrise300/timelapse-b.mp4"
        new_file_a = "/home/pi/sunrise300/" + strftime("%d-%B-%h-%m-a")+".mp4"
        new_file_b = "/home/pi/sunrise300/" + strftime("%d-%B-%h-%m-b")+".mp4"
        subprocess.call(f"mv {old_file_a} {new_file_a}", shell = True)
        subprocess.call(f"mv {old_file_b} {new_file_b}", shell = True)
        subprocess.call(f"rm -r {old_file_a}", shell = True)
        subprocess.call(f"rm -r {old_file_b}", shell = True)
    return new_file_a, new_file_b

def upload(file_A, file_B):
    with open(file_A, "rb") as f:
        dbx.files_upload(f.read(), filename, mute = True)
    with open(file_B, "rb") as f:
        dbx.files_upload(f.read(), filename, mute = True)
if __name__ == "__main__":
    fileA, fileB = rename()
    upload(fileA, fileB)
