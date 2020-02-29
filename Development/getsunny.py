from astral import LocationInfo
from datetime import datetime, timedelta

# l = LocationInfo('name', 'region', 'timezone/name', 0.1, 1.2)

city = LocationInfo("Newcastle Upon Tyne", "England", "Europe/London", 55.0464, 1.4513)
now_time = datetime.time(datetime.now())

from astral.sun import sun
s = sun(city.observer, date=datetime.date(datetime.now()))

# print((
#     f'Dawn:    {s["dawn"]}\n'
#     f'Sunrise: {s["sunrise"]}\n'
#     f'Noon:    {s["noon"]}\n'
#     f'Sunset:  {s["sunset"]}\n'
#     f'Dusk:    {s["dusk"]}\n'
# ))

# print(s['sunrise'].time())
sunrise_time = s['sunrise']
# print(datetime.time(datetime.now()))
print(sunrise_time)
# lapse_start_time = datetime.time(datetime.now()) + timedelta(minutes=100)

# print(lapse_start_time)

lapse_start_time = sunrise_time - timedelta(minutes=100)

print(lapse_start_time)