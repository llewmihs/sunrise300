from glob import glob
import dropbox
from config import *

files = glob('*.jpg')

# set up dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

for i in range(len(files)):
    print('Uploading file %s' % files[i])
    with open(files[i], "rb") as f:
        dbx.files_upload(f.read(), "/" + files[i], mute = True)

