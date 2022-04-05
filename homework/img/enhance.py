from PIL import Image, ImageDraw, ImageFilter
import math
import sys

def main():
    try:
        image=Image.open("IMG_0600.jpg")
    except:
        print("Error in opening image file.")
        sys.exit()
    cropbox=(1200, 2400, 2400, 3600)
    xsize, ysize = image.size
    if (cropbox[0]>xsize or cropbox[2]>xsize):
        print("Error: box outside x range")
        sys.exit()
    if (cropbox[1]>ysize or cropbox[3]>ysize):
        print("Error: box outside y range")
        sys.exit()
    part=image.crop(cropbox)
    for i in range(5):
        image=image.filter(ImageFilter.BLUR)
    part=part.filter(ImageFilter.EDGE_ENHANCE_MORE)
    image.paste(part, cropbox)
    draw=ImageDraw.Draw(image)
    draw.rectangle(cropbox, outline='black')
    image.show()
    image.save("IMG_0600_edge.jpg")

main()