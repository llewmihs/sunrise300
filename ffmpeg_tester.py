import subprocess
import os.path
from time import time
import logging
import dropbox 
from config import *
from glob import glob

dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)
logging.basicConfig(filename='ffmpeg_test.log',level=logging.DEBUG)
logging.info('Begin ffmpeg test')

def test_lapser():
    presets = ['slow','veryslow']
    # CRF ranges 17 - 25
    for i in range(17,25,2):
        for j in presets:
            fl = f"TEST-crf-{i}-preset-{j}.mp4"
            start_time = time()
            subprocess.call(f"ffmpeg -y -r 15 -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset {j} -crf {i} {fl}", shell=True)
            end_time = time()
            elapsed_time_mins = int((end_time - start_time)/60)
            file_in_mb = int(os.path.getsize(fl)/((1024*1024)))
            logging.info(f"File: {fl}. Size: {file_in_mb} mb. Time {elapsed_time_mins} mins")
            
def files_getter():
    fl = glob("/home/pi/sunrise300/*.mp4")
    print(fl)
    return fl

def upload_db(mp4_file):
    with open(mp4_file, "rb") as f:
        print(f"Uploading file {mp4_file}")
        dbx.files_upload(f.read(), mp4_file)
    
if __name__ == "__main__":
    test_lapser()
    fl = files_getter()
    for i in fl:
        upload_db(i)
    # start_time = time()
    # print(f"Attempting to compile video file - < {video} > - using FFMPEG")
    # print(".........................................................")
    # subprocess.call(f"ffmpeg -y -r {frames} -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset {preset} -crf {crf} {video}", shell=True)
    # end_time = time()
    # elapsed_time_secs = int(end_time - start_time)
    # elapsed_time_mins  = int(elapsed_time_secs / 60)
    # print(f"Programme executed in {elapsed_time_mins} minutes")

    # if os.path.exists(video): # has the file been written, and is it of a decent size?
    #     print(f"SUCCESS - FFMPEG created the video file: {video}")
    #     file_in_mb = int(os.path.getsize(video)/((1024*1024)))
    #     print(f"Fileseize: ~ {file_in_mb} Mb")

    # else:
    #     print(f"ERROR - FFMPEG failed to create the video file: {video}")
    #     print(f"Programme exiting early")