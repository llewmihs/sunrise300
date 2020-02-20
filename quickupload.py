import dropbox
import os
from config import *

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

file_path = "timelapse.avi"

with open(file_path, "rb") as f:
    dbx.files_upload(f.read(), "/" + file_path, mute = True)