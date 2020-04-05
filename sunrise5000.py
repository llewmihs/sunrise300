from time import sleep, strftime, time
from picamera import PiCamera
from config import *
import dropbox

#dropbox, timeout=none allows for uploading of larger files without 30second normal timeout
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None) 

# the Picamera, at full resolution
camera = PiCamera()
camera.resolution = (3280, 2464)

def timelapse_calculations(duration):
    duration_seconds = duration * 60
    film_length_seconds = 30
    frame_rate = 30
    total_number_of_frames = film_length_seconds * frame_rate
    delay_between_images = duration_seconds / total_number_of_frames
    return total_number_of_frames, delay_between_images

def take_a_picture(num_of_frames, time_between_images):
    print("Taking a photo")
    camera.start_preview()
    sleep(2)
    for i in num_of_frames:
        file_name = 'IMAGE_' '{0:04d}'.format(i)+".JPG"
        full_path = "/home/pi/sunrise300/images/" + file_name
        camera.capture(full_path)
        sleep(time_between_images)
    camera.stop_preview()

def  upload_to_dropbox(filepath, filename):
    print("Uploading to Dropbox")
    dropbox_filepath = "/SunriseImages/"+filename
    with open(filepath, "rb") as f:
        dbx.files_upload(f.read(), dropbox_filepath, mute = True)

def ffmpeg_creation():
    

if __name__ == "__main__":
    i, j = take_a_picture()
    upload_to_dropbox(i,j)