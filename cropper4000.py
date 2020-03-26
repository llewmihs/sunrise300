from glob import glob
from PIL import Image
import progressbar
from config import *    # my dropbox API key and Push bullet API key
from pushbullet import Pushbullet   # notification software to monitor the programme remotely `pip3 install pushbullet.py`
pb = Pushbullet(PUSHBULLET)

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

if __name__ == "__main__":
    push = pb.push_note("Images taken successfully", "Commencing crop")

    #the_cropper()