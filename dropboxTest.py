import dropbox
from config import *

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

#print(dbx.users_get_current_account())

with open("/Users/joe/Desktop/sunrise300/test.txt", "rb") as f:
    dbx.files_upload(f.read(), '/test.txt', mute = True)