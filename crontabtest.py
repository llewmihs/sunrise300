from crontab import CronTab
from datetime import datetime, timedelta    # for the current time and adding time
import pytz                         # to enale comparison of datetime and astral time, astral is ofset, datetime is naive
from astral import LocationInfo     # to get the location info
from astral.sun import sun          # to get the sunrise time

# ofset setting
utc=pytz.UTC
now = utc.localize(datetime.now())
my_cron = CronTab(user='pi')

# set Astral location for Whitley Bay
city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, 1.4513)

# get today's sunrise time
s = sun(city.observer, date=datetime.date(datetime.now()))
print("Today's sunrise is at:")
print(s['sunrise'])

job = my_cron.new(command='nohup python3 /home/pi/justpics.py &')

job.hour.on(2)
job.minute.on(10)

my_cron.write()

for job in my_cron:
    print(job)