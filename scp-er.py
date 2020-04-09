import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime

def rename():
    filename = strftime("%d-%B-%h-%m") + ".mp4"
    subprocess.call(f"mv /home/pi/sunrise300/timelapse.mp4 /home/pi/sunrise300/{filename}")
    return filename

def scp_transfer(password, address, filename):
    subprocess.call(f"")