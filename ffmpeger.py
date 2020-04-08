from glob import glob
import subprocess
from time import strftime, sleep
import dropbox      # for uploading to dropbox, `pip3 install dropbox`
from config import *    # my dropbox API key and Push bullet API key
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) #dropbox, timeout=none allows for uploading of larger files without 30second normal timeout

def big_file_creator(filename):
    subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {filename}",shell = True)

def big_file_splitter(filename):
    chunks = ['00:00:00','00:00:05','00:00:10','00:00:15','00:00:20','00:00:25','00:00:30']
    new_filename = strftime("%d-%b-")
    for i in range(len(chunks)-1):
        new_file = new_filename + str(i) + ".mp4"
        subprocess.call(f"/usr/local/bin/ffmpeg -ss {chunks[i]} -t {chunks[i+1]} -i {filename} -acodec copy -vcodec copy {new_file}",shell = True)
    subprocess.call(f"rm -r /home/pi/sunrise300/timelapse.mp4", shell = True)

def upload_to_dropbox():
    mp4_files = glob("/home/pi/sunrise300/*.mp4")
    dbx_daily_folder = "/sunrises/" + strftime("%d-%b") + "/"
    for i in range(len(mp4_files)):
        dbx_daily_filename = dbx_daily_folder + mp4_files[i][20:]
        with open(mp4_files[i], "rb") as f:
            dbx.files_upload(f.read(), dbx_daily_filename, mute = True)
        sleep(60)

if __name__ == "__main__":
    big_file_creator("timelapse.mp4")
    big_file_splitter("timelapse.mp4")