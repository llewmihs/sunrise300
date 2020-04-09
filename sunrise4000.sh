#!/bin/sh

# navigate to the Sunrise300 folder
cd /home/pi/sunrise300

# clean up the folders
rm -r /home/pi/sunrise300/set1/*.JPG
rm -r /home/pi/sunrise300/set2/*.JPG
rm -r /home/pi/sunrise300/*.mp4

# calculate the timelapse details and take all the images
python3 camera4000.py

# crop all the images
python3 cropper4000.py

# ffmpeg the files
/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number 0000 -i /home/pi/sunrise300/IMAGE_%04d.JPG  -vcodec libx264 -preset slow -crf 17 timelapse-a.mp4

# update the crontab
python3 crontab4000.py

# dropbox upload
python3 dropbox4000.py