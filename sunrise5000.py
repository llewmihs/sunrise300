# step 1 import the modules (there's a few)

# function declarations
def lapse_details(duration_in_minutes, fps):    # calculate the total number of frames needed - this is a little moot
    print(f"User lapse duration request: {duration_in_minutes} minutes.")
    real_time = duration_in_minutes * 60 # minutes * 60 seconds
    film_length = 30
    frame_rate = fps
    total_frames = film_length * frame_rate
    delay = real_time / total_frames
    return total_frames, delay

def the_camera(no_of_frames, delay):
    camera.start_preview()
    sleep(2) # Camera warm-up time
    for i in progressbar.progressbar(range(no_of_frames)):
        file_path = "/home/pi/sunrise300/images/" + 'IMAGE_' '{0:04d}'.format(i)+".JPG" #create timestamp filename
        camera.capture(file_path)
        sleep(delay)
    camera.stop_preview()

def the_cropper():

    # Setting the points for cropped image 
    left = 0
    upper = 0
    right = 1640
    lower = 922
    print(".........................................................")
    print(f"Croppping files to new res: {right} by {lower}")
    file_list = glob("/home/pi/sunrise300/images/*.JPG")
    for names in progressbar.progressbar(file_list):
        im = Image.open(names)
        im = im.crop((left, upper, right, lower))
        im.save(names)

def ffmpeg_lapser():
    