from datetime import datetime, timedelta
from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time

def get_sunrise_and_sunset():
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, -1.4513)
    s = sun(city.observer, date=localize(datetime.date(datetime.now())))
    print(s['sunrise'])
    suntime_0 = s['sunrise'] - timedelta(minutes=60)
    suntime_1 = s['sunrise'] + timedelta(minutes=30)
    suntime_2 = s['sunset'] - timedelta(minutes=60)
    suntime_3 = s['sunset'] + timedelta(minutes=30)
    print(f"0 - {suntime_0}, 1 - {suntime_1}, 2 - {suntime_2}, 3 - {suntime_3}, ")


if __name__ == "__main__":
    get_sunrise_and_sunset()