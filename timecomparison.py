from datetime import datetime, timedelta

# astral is an 'offset aware' datetime, so we need to turn datetime into 'offset aware'
import pytz
utc=pytz.UTC

now = utc.localize(datetime.now())
print("Current time:")
print(now)

from astral import LocationInfo
from astral.sun import sun

# set Astral location for Whitley Bay
city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, 1.4513)

# get today's sunrise time
s = sun(city.observer, date=datetime.date(datetime.now()))

print(s['sunrise'])

sunrise_time = s['sunrise']

# get the timelapse start time
lapse_window_open = sunrise_time - timedelta(minutes=100)
lapse_window_closed = sunrise_time - timedelta(minutes=90)


print(now < lapse_window_open)
print(now == lapse_window_open)
print(now > lapse_window_open)
