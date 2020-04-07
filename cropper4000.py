from glob import glob
from PIL import Image
from config import *    # my dropbox API key and Push bullet API key
pb = Pushbullet(PUSHBULLET)

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

 def image_move():
     file_list = glob("/home/pi/sunrise300/images/*.JPG")
     number_of_files = len(file_list)
     print(number_of_files)


if __name__ == "__main__":
    image_move():