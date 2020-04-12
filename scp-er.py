import subprocess # to run file cleanup after the upload
from config import *    # my dropbox API key and Push bullet API key
from time import strftime
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)

def rename():
    filename = strftime("%d-%B-%H%M") + ".mp4"
    subprocess.call(f"mv /home/pi/sunrise300/timelapse.mp4 /home/pi/sunrise300/{filename}", shell = True)
    print("File renamed")
    return filename

def scp_copy(filename, password, localpath):
    subprocess.call(f"sshpass -p {password} scp {filename} {localpath}", shell = True)
    print("File uploaded")

if __name__ == "__main__":
    filename = rename()
    scp_copy(filename, password, localpath)
    push = pb.push_note("Job Done", "Full programme has now run.")
    