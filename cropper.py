from PIL import Image
im = Image.open("testimage.jpg")

print(im.format, im.size, im.mode)

box = (0,265,2160,1480)

region = im.crop(box)
region.save("testimage.jpg")
