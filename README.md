# sunrise300

## Overview

The sunrise3000 is a Raspberry Pi timelapse camera which builds a timelapse video of sunrise each day and uploads to dropbox

## Dependencies

The following modules are needed:

* dropbox `pip3 install dropbox`
* pushbullet `pip3 install pushbullet.py`
* astral `pip3 install astral`
* python-crontab `pip3 install python-crontab`

### Dropbox

To use dropbox from python, you'll need to find your API Access Token, create an app first: https://www.dropbox.com/developers/apps

Then in python:

``` python
import dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)
```

We need to set `timeout=None` to enable uploads of large files that will take longer than the default timeout of 30 seconds.

To upload a file to dropbox:

``` python
with open(filepath, "rb") as f:
    dbx.files_upload(f.read(), filepath, mute = True)
```

### Pushbullet

Pushbullet is smartphone notification software. Install on your smartphone and then head to https://www.pushbullet.com/#settings/account to get your access token.

Then in python:

``` python
from pushbullet import Pushbullet
pb = Pushbullet(Pushbullet_key)
push = pb.push_note("The Timelapse Has Started at time", "Fun times")
```

### Astral

Astral will allow me to get the time of sunrise from any location on Earth.

In python:

``` python
from datetime import datetime, timedelta # to get current time and add/subtract time
from astral import LocationInfo     # to get the location info 
from astral.sun import sun          # to get the sunrise time
city = LocationInfo("Your city", "Your country", "Europe/London", degrees_North, degrees_West)
s = sun(city.observer, date=datetime.date(datetime.now())+timedelta(days=1))
sunrise_time = s['sunrise'] 
# timelapse shoudl start 1 hour prior
timelapse_start = sunrise_time - timedelta(minutes=60)
```

### Python-crontab

The timelapser should start at 40 minutes before sunrise each day. I want to automate the process, so at the end of each run the script updates the crontab for the next day's lapse.

In python:

``` python
from crontab import CronTab
my_cron = CronTab(user='pi')
my_cron.remove_all()    # clear current crontab
# set the cron job to run in the background
job = my_cron.new(command='nohup python3 /home/pi/sunrise300/sunrise3000.py &')
job.hour.on(timelapse_start.hour)
job.minute.on(timelapse_start.minute)
my_cron.write() #write the job to the crontab
```

The command is worth further explanation:

* `nohup` will run the programme even if the ssh is exited - this was mainly for testing purposes
* `&` runs the programme in the background

## Building a timelapse using FFMPEG

This is a bit of a nightmare, espcially as my setup is on a Pi Zero W. This makes compiling and installing FFMPEG a time consuming process. As a result the current build of the Sunrise3000 can only create video files in .mov prores formats! The commands to build an .mp4 with h264 codec fail, and because a rebuild takes the best part of the day I dont have the patient to test it.
