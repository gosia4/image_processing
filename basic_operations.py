import numpy as np
from PIL import Image
import math
import support_functions as sp


def modify_brightness(image, factor):
    if factor < -255:
        factor = -255
    if factor > 255:
        factor = 255

    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("this program does not support this color model.")
        return

    for y in range(height):
        for x in range(width):
            color_tab = []
            for c in range(color_channels):
                old_value = image.getpixel((x, y))
                # appends new color value once for each color channel
                color_tab.append(factor + sp.int_or_tuple_to_array(old_value)[c])

            # then puts that pixel to the new image as a tuple (I hate tuples)
            result_image.putpixel((x, y), tuple(color_tab))
    result_image.save("new_image.bmp")
    result_image.show()


def modify_contrast(image, factor):
    if factor > 10:
        factor = 10
    if factor < -10:
        factor = -10

    lut = []
    # creates a look up table (all 256 possible transformations)
    for i in range(256):
        new = 128 + ((i - 128) * (math.e ** factor))
        lut.append(new)

    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("this program does not support this color model.")
        return

    for y in range(height):
        for x in range(width):
            color_tab = []
            for c in range(color_channels):
                old_value = image.getpixel((x, y))
                # appends new color value once for each color channel
                color_tab.append(int(lut[sp.int_or_tuple_to_array(old_value)[c]]))

            # then puts that pixel to the new image as a tuple (I hate tuples)
            result_image.putpixel((x, y), tuple(color_tab))
    result_image.save("new_image.bmp")
    result_image.show()


def apply_negative(image):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("this program does not support this color model.")
        return

    for y in range(height):
        for x in range(width):
            color_tab = []
            for c in range(color_channels):
                old_value = image.getpixel((x, y))
                # appends negative color value once for each color channel
                color_tab.append(int(255 - sp.int_or_tuple_to_array(old_value)[c]))

            # then puts that pixel to the new image as a tuple (I hate tuples)
            result_image.putpixel((x, y), tuple(color_tab))

    result_image.show()
    result_image.save("new_image.bmp")
