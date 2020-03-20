from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
from config import *    # my dropbox API key and Push bullet API key
import sys
import subprocess

pb = Pushbullet(PUSHBULLET)

feed = sys.argv[1]
value = sys.argv[2]

push = pb.push_note(f"The feed is {feed}", f"Value: {value}")

subprocess.call("touch test.txt", shell=True)