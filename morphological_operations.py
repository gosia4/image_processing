import support_functions as sp

from PIL import Image
import numpy as np


def dilation(image, output = None):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    one_bit_image_array = np.array(image)

    white_pixel_found = False

    for x in range(width):
        for y in range(height):

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if one_bit_image_array[target_x][target_y]:
                            result_image.putpixel((y, x), 1)
                            white_pixel_found = True
                            break
                if white_pixel_found:
                    white_pixel_found = False

    result_image.show()


def erosion(image, output = None):
    width, height = image.size
    result_image = Image.new('1', (width, height), 1)
    one_bit_image_array = np.array(image)

    black_pixel_found = False

    for x in range(width):
        for y in range(height):

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if one_bit_image_array[target_x][target_y] == 0:
                            result_image.putpixel((y, x), 0)
                            black_pixel_found = True
                            break
                if black_pixel_found:
                    black_pixel_found = False

    result_image.show()
