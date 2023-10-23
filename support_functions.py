import numpy as np
from PIL import Image
import time

time_start = 0
# saves the image to the desired path
def save_image(image, output_path):
    image.save(output_path)

# gets the variable (item) that can be either int or RGB pixel format (tuple of 3-element arrays)
#   returns a list of either 1 item (Grayscale int) or 3 items (RGB int values)
def process_int_or_tuple(item):
    if type(item) is tuple:
        return np.array(item)
    else:
        return (item, item, item)


# reads the color mode of the image
#   returns new empty canvas with apropriate format (mode) [Grayscale / RGB]
#   returns number of color channels this image has
def analyse_color_channels(image):
    width, height = image.size
    if image.mode == "RGB":
        return [Image.new('RGB', (width, height)), 3]
    elif image.mode == "L":
        return [Image.new('L', (width, height)), 1]
    else:
        print("this program does not support this color model.")
        return [0, 0]


def measure_time(start):
    global  time_start
    if start:
        time_start = time.time()
        return
    else:
        print(time.time() - time_start)


