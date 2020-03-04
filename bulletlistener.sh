#!/bin/bash
cd /home/pi/sunrise300
pblisten --exec ping.py --key-file creds.txt --throttle-count 1 --throttle-seconds 10
