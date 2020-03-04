#!/bin/bash
cd /home/pi/sunrise300
pblisten --exec /home/pi/sunrise300/ping.py --key-file /home/pi/sunrise300/creds.txt --throttle-count 1 --throttle-seconds 10
