import dropbox
from config import *

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN)

#print(dbx.users_get_current_account())

with open("test2.txt", "rb") as f:
    dbx.files_upload(f.read(), '/test2.txt', mute = True)