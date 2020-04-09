from glob import glob
from PIL import Image
from config import *    # my dropbox API key and Push bullet API key
import subprocess

def the_cropper():
    # Setting the points for cropped image 
    left = 0
    upper = 0
    right = 3200
    lower = 1800
    print(".........................................................")
    print(f"Croppping files to new res: {right} by {lower}")
    file_list = glob("/home/pi/sunrise300/images/*.JPG")
    for names in file_list:
        im = Image.open(names)
        im = im.crop((left, upper, right, lower))
        im.save(names)

if __name__ == "__main__":
    the_cropper()