from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
from time import sleep, strftime

# set Astral location for Whitley Bay
city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.0464, 1.4513)





if __name__ == "__main__":
    while True:
        print("Checking the suntime, and now time")
        # get the current time
        now_time = datetime.time(datetime.now())
        
        # get the sunrise time for today
        s = sun(city.observer, date=datetime.date(datetime.now()))
        sunrise_time = s['sunrise']
        
        # get the timelapse start time
        lapse_window_open = sunrise_time - timedelta(minutes=100)
        lapse_window_closed = sunrise_time - timedelta(minutes=90)
        
        # compare the current time to the sunrise time
        if lapse_window_open <= now_time <= lapse_window_closed:
            print("Starting the timelapse")
        
        # wait 5 minutes before you check again
        sleep(5)



