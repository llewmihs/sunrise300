import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from config import *    # my dropbox API key and Push bullet API key
import sys

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

def upload(oldfile, filename):
    filename = "/" + filename
    with open(oldfile, "rb") as f:
        dbx.files_upload(f.read(), filename, mute = True)

if __name__ == "__main__":
    upload(sys.argv[1],sys.argv[2])