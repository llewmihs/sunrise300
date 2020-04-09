import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime

def rename():
    filename = strftime("%d-%B-%h-%m") + ".mp4"
    subprocess.call(f"mv /home/pi/sunrise300/timelapse.mp4 /home/pi/sunrise300/{filename}")
    print("File renamed")
    return filename

def scp_copy(filename, password, localpath):
    subprocess.call(f"sshpass -p {password} scp {filename} {localpath}", shell = True)
    print("File uploaded")

if __name__ == "__main__":
    filename = rename()
    scp_copy(filename, password, localpath)