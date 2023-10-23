import numpy as np
from PIL import Image
import math
import support_functions as sp


def modify_brightness(image, factor, output):

    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("this program does not support this color model.")
        return

    for y in range(height):
        for x in range(width):
            color_tab = []
            old_value = image.getpixel((x, y))
            for c in range(color_channels):
                # appends new color value once for each color channel
                color_tab.append(int(factor) + sp.process_int_or_tuple(old_value)[c])

            # then puts that pixel to the new image as a tuple (I hate tuples)
            result_image.putpixel((x, y), tuple(color_tab))
    sp.save_image(result_image, output)
    result_image.show()


def modify_contrast(image, factor, output):
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
            old_value = image.getpixel((x, y))
            for c in range(color_channels):
                # appends new color value once for each color channel
                color_tab.append(int(lut[sp.process_int_or_tuple(old_value)[c]]))
            # then puts that pixel to the new image as a tuple (I hate tuples)
            result_image.putpixel((x, y), tuple(color_tab))
    sp.save_image(result_image, output)
    result_image.show()


def apply_negative(image, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("this program does not support this color model.")
        return

    for y in range(height):
        for x in range(width):
            color_tab = []
            old_value = image.getpixel((x, y))
            for c in range(color_channels):
                # appends negative color value once for each color channel
                color_tab.append(int(255 - sp.process_int_or_tuple(old_value)[c]))

            # then puts that pixel to the new image as a tuple (I hate tuples)
            result_image.putpixel((x, y), tuple(color_tab))
    sp.save_image(result_image, output)
    result_image.show()
