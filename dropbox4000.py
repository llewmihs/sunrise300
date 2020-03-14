import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from config import *    # my dropbox API key and Push bullet API key
import subprocess # to run file cleanup after the upload
from glob import glob # for the file upload process
from time import sleep, strftime, time # for the picamera and to name the files

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

def rename():
    glob_file = glob("/home/pi/sunrise300/*.mp4")[0]
    new_file = "/home/pi/sunrise300/" + strftime("%d%B")+".mp4"
    subprocess.call(f"cp {glob_file} {new_file}", shell = True)
    return new_file

def upload(filename):
    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), filename, mute = True)

if __name__ == "__main__":
    mp4file = rename()
    upload(mp4file)