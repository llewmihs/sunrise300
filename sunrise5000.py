from datetime import datetime, timedelta, strftime
from astral import LocationInfo     # to get the location info `pip3 install astral`
from astral.sun import sun          # to get the sunrise time
#from picamera import PiCamera # raspberry pi camera
import pytz
utc=pytz.UTC

from time import sleep
import subprocess
# the Picamera
#camera = PiCamera()
#camera.resolution = (3280, 2464)

def get_sunrise_and_sunset():
    city = LocationInfo("Whitley Bay", "England", "Europe/London", 55.051331, -1.451146)
    s = sun(city.observer, date=(datetime.date(datetime.now())))
    # correct for GMT vs UCT
    sunrise = s['sunrise'] + timedelta(minutes=60)
    sunset = s['sunset'] + timedelta(minutes=60)
    return sunrise, sunset

def calculate_the_lapse_windows(sunrise, sunset):
    #-------T0-----sunrise---------T1-------------T2-----sunset----------T3
    #---- -1hr --------------- +30mins ------- -1hr --------------- +30mins
    T0 = sunrise - timedelta(minutes=60)
    T1 = sunrise + timedelta(minutes=30)
    T2 = sunset - timedelta(minutes=60)
    T3 = sunset + timedelta(minutes=30)
    return T0, T1, T2, T3

def photo_delay_calculations(time_x, time_y, vid_length):
    frames = vid_length * 30
    delay = (time_y - time_x)/frames
    time_string = str(delay)
    delay = int(time_string[-2:])
    return delay

def auto_camera(delay, vid_length, folder):
    print(f"Starting the {folder} timelapse")
    camera.start_preview()
    sleep(2) 
    for i in range(vid_length*30):
        file_path = "/home/pi/sunrise300/" + folder + 'IMAGE_' + '{0:04d}'.format(i)+".JPG"
        camera.capture(file_path)
        sleep(delay)
    camera.stop_preview()
    return True

def ffmpeg_creation():
    filepath = "/home/pi/sunrise300/images/IMAGE__%04d.JPG"
    subprocess.call(f"/usr/local/bin/ffmpeg -y -r 30 -f image2 -start_number 0000 -i {filepath} -vcodec libx264 -preset slow -crf 17 timelapse.mp4", shell = True)
    newfilename = strftime("%d-%B-%h-%m")+".mp4"
    subprocess.call(f"mv timelapse.mp4 {newfilename}", shell = True)

def scp_copy(filename, password, localpath):
    subprocess.call(f"sshpass -p {password} scp {filename} {localpath}", shell = True)


if __name__ == "__main__":
    sunrise, sunset = get_sunrise_and_sunset()

    T0, T1, T2, T3 = calculate_the_lapse_windows(sunrise, sunset)

    sunrise_frame_delay = photo_delay_calculations(T0, T1, 30)
    daytime_frame_delay = photo_delay_calculations(T1, T2, 30)
    sunset_frame_delay = photo_delay_calculations(T2, T3, 30)
    
    run = True

    sunrise_done = False
    daytime_done = False
    sunset_done = False

    while run:
        current_time = utc.localize(datetime.now())
        if current_time > T0 and current_time < T1 and sunrise_done = False:
            sunrise_done = auto_camera(sunrise_frame_delay, 30, "sunrise")

        elif current_time > T1 and current_time < T2 daytime_done = False:
            daytime_done = auto_camera(daytime_frame_delay, 30, "daytime")

        elif current_time > T2 and current_time < T3 sunset_done = False:
            run = auto_camera(daytime_frame_delay, 30, "sunset")
        else:
            pass
    
    # if we've got here then we've taken everything for a day
    # let's ffmpeg!!!
    


            
