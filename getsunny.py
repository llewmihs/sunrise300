from astral import LocationInfo
import datetime

# l = LocationInfo('name', 'region', 'timezone/name', 0.1, 1.2)

city = LocationInfo("Newcastle Upon Tyne", "England", "Europe/London", 55.0464, 1.4513)


from astral.sun import sun
s = sun(city.observer, date=datetime.date(2009, 4, 22))

print((
    f'Dawn:    {s["dawn"]}\n'
    f'Sunrise: {s["sunrise"]}\n'
    f'Noon:    {s["noon"]}\n'
    f'Sunset:  {s["sunset"]}\n'
    f'Dusk:    {s["dusk"]}\n'
))