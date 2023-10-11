import numpy as np
from PIL import Image
import image_processing.venv.support_functions as sp


def horizontal_flip(image):
    width, height = image.size
    result_image = sp.analyse_color_channels(image)[0]

    for y in range(height):
        for x in range(width//2): # divide by 2 to avoid transforming the same elements multiple times
            left_pixel = image.getpixel((x, y))
            right_pixel = image.getpixel((width - x - 1, y))
            result_image.putpixel((x, y), right_pixel)
            result_image.putpixel((width - x - 1, y), left_pixel)
    result_image.save("new_image.bmp")
    result_image.show()


def vertical_flip(image):
    width, height = image.size
    result_image = sp.analyse_color_channels(image)[0]
    for y in range(height//2):
        for x in range(width):
            top_pixel = image.getpixel((x,y))
            bottom_pixel = image.getpixel((x, height - y - 1))
            result_image.putpixel((x,y), bottom_pixel)
            result_image.putpixel((x, height - y - 1), top_pixel)
    result_image.save("new_image.bmp")
    result_image.show()


def diagonal_flip(image):
    width, height = image.size
    result_image = sp.analyse_color_channels(image)[0]
    for x in range(width):
        for y in range(height):
            result_image.putpixel((width - x - 1, height - y - 1), image.getpixel((x, y)))
    result_image.save("new_image.bmp")
    result_image.show()

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
        scaled_image.show()

def shrink(image):
    result_image = sp.analyse_color_channels(image)[0]
    # result_image = image
    width, height = image.size
    move_distance = width // 4
    for x in range(width // 4, width - width // 4):
        move_distance -= 1
        for y in range(height):
            temp = []
            result_image.putpixel((x,y), image.getpixel((x - move_distance,y)))
    result_image.show()



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
    scaled_image.show()


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
    enlarged_img.show()