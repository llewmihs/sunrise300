from datetime import datetime, timedelta
from time import sleep

# astral is an 'offset aware' datetime, so we need to turn datetime into 'offset aware'
import pytz
utc=pytz.UTC

now = utc.localize(datetime.now())
print("Current time:")
print(now)

# get the timelapse start time
lapse_window_open = now + timedelta(minutes=0.5)
lapse_window_closed = now + timedelta(minutes=1)

while True:
    print("Testing at Now %s" % utc.localize(datetime.now()))
    print("Lapse window open at %s" % lapse_window_open)
    print(utc.localize(datetime.now()) < lapse_window_open)
    print(utc.localize(datetime.now()) > lapse_window_open)
    if lapse_window_open < utc.localize(datetime.now()) < lapse_window_closed:
        print("The Golden Window is Open")
    print("")
    sleep(5)
