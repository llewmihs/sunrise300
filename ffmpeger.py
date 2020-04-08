from glob import glob
import subprocess
from time import strftime

def big_file_creator(filename):
    subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 {filename}",shell = True)

def big_file_splitter(filename):
    chunks = ['00:00:00','00:00:05','00:00:10','00:00:15','00:00:20','00:00:25','00:00:30']
    new_filename = strftime("%d-%b-")
    for i in range(len(chunks)-1):
        new_file = new_filename + str(i) + ".mp4"
        subprocess.call(f"ffmpeg -ss {chunks[i]} -t {chunks[i+1]} -i {filename} -acodec copy -vcodec copy {new_file}",shell = True)

if __name__ == "__main__":
    big_file_creator("timelapse.mp4")
    big_file_splitter("timelapse.mp4")