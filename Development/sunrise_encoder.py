import subprocess
import dropbox
#from config import *
from time import strftime

# set up dropbox
#dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)

vid_path = "/home/pi/sunrise300/videos/" + strftime("%Y%m%d")+".mp4"
vid_path = strftime("%Y%m%d")+".mp4"

def create_timelapse(filepath):
    try:
        #subprocess.call("mencoder mf://home/pi/sunrise300/images/*.jpg -nosound -of lavf -lavfopts format=mp4 -ovc x264 -x264encopts pass=1:bitrate=2000:crf=24 -o %s -mf type=jpg:fps=15" % filepath ,shell=True)
        subprocess.call("avconv -r 10 -i /home/pi/sunrise300/images/*.jpg -r 15 -vcodec libx264 -vf scale=1280:720 timelapse.mp4", shell=True)
    except:
        print("Failure to create video file")

def upload_to_dropbox(filepath):
    try:
        with open(filepath, "rb") as f:
            dbx.files_upload(f.read(), filepath, mute = True)
    except:
        print("Failure to upload the file to Dropbox")

def clean_up():
    subprocess.call("rm -r /home/pi/sunrise300/images/*.jpg", shell=True)

if __name__ == "__main__":
    create_timelapse(vid_path)