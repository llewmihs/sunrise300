#!/bin/sh
cd /home/pi/sunrise300 &&
ffmpeg -y -r 30 -f image2 -start_number 0000 -i /home/pi/sunrise300/images/IMAGE_%04d.JPG -vcodec libx264 -preset slow -crf 17 14march.mp4