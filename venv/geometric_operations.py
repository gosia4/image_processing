import numpy as np
from PIL import Image

im = Image.open("venv/images/lenac.bmp")
arr = np.array(im.getdata())
if arr.ndim == 1:  # grayscale
    numColorChannels = 1
    arr = arr.reshape(im.size[1], im.size[0])
else:
    numColorChannels = arr.shape[1]
    arr = arr.reshape(im.size[1], im.size[0], numColorChannels)
def horizontal_flip(image):
    width, height = image.size
    flipped_image = Image.new('RGB', (width, height))

    for y in range(height):
        for x in range(width//2): # divide by 2 to avoid transforming the same elements multiple times
            left_pixel = image.getpixel((x, y))
            right_pixel = image.getpixel((width - x - 1, y))
            flipped_image.putpixel((x, y), right_pixel)
            flipped_image.putpixel((width - x - 1, y), left_pixel)
    flipped_image.save("new_image.bmp")


def vertical_flip(image):
    width, height = image.size
    flipped_image = Image.new('RGB', (width, height))
    for y in range(height//2):
        for x in range(width):
            top_pixel = image.getpixel((x,y))
            bottom_pixel = image.getpixel((x, height - y - 1))
            flipped_image.putpixel((x,y), bottom_pixel)
            flipped_image.putpixel((x, height - y - 1), top_pixel)
    flipped_image.save("new_image.bmp")


def diagonal_flip(image):
    width, height = image.size
    flipped_image = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            flipped_image.putpixel((width - x - 1, height - y - 1), image.getpixel((x, y)))
    flipped_image.save("new_image.bmp")

def shrinking(image, factor):
    if factor == 0:print("You cannot divide by zero")
    else:
        width, height = image.size
        new_width = int(width / factor)
        new_height = int(height / factor)
        scaled_image = Image.new('RGB', (new_width, new_height))
        for y in range(new_height):
            for x in range(new_width):
                scaled_image.putpixel((x, y), tuple(image.getpixel((int(x*factor), int(y*factor)))))
        scaled_image.save("new_image.bmp")

def enlarge(image, factor):
    width, height = image.size
    new_width = int(width * factor)
    new_height = int(height * factor)
    scaled_image = Image.new('RGB', (new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            #scaled_image.putpixel((x, y), tuple(image.getpixel((int(x / factor), int(y / factor)))))
            for z in range(3):
                scaled_image.putpixel((x, y), tuple(image.getpixel((int(x / factor), int(y / factor))))) # tuple - podobne do list
    scaled_image.save("new_image.bmp")


def enlarge_image(img, val):
    print("Enlarge by:", val)
    original_width, original_height = img.size
    new_width = int(original_width * val)
    new_height = int(original_height * val)

    enlarged_img = Image.new('RGB', (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):
            for z in range(3):
                enlarged_img.putpixel((x, y), tuple(img.getpixel((int(x / val), int(y / val)))))
    enlarged_img.save("new_image.bmp")