import dropbox 
from config import *
from glob import glob
from time import time
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

def files_getter():
    fl = glob("/home/pi/sunrise300/*.mp4")
    print(fl)
    return fl

def upload_db(mp4_file):
    with open(mp4_file, "rb") as f:
        print(f"Uploading file {mp4_file}")
        dbx.files_upload(f.read(), mp4_file)

if __name__ == "__main__":
    fl = files_getter()
    for i in fl:
        upload_db(i)

