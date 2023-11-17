import numpy as np
from PIL import Image
import time
from matplotlib import pyplot as plt

# global measure_time function flag-variable
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
        return item, item, item

def int_or_tuple_to_list(item):
    if type(item) is tuple:
        return list(item)
    else:
        return [item]


# reads the color mode of the image
#   returns new empty canvas with appropriate format (mode) [Grayscale / RGB]
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
    global time_start
    if start:
        time_start = time.time()
        return
    else:
        print(time.time() - time_start)


def create_histogram(image):
    width, height = image.size
    color_channels = analyse_color_channels(image)[1]

    if color_channels == 1:
        histogram = [[0] * 256]  # Create a histogram with 256 ints.
        for x in range(width):
            for y in range(height):
                pixel_value = image.getpixel((x, y))
                histogram[0][pixel_value] += 1
        return histogram

    elif color_channels == 3:
        histogram = [[0] * 256 for _ in range(3)]

        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                histogram[0][r] += 1
                histogram[1][g] += 1
                histogram[2][b] += 1
        return histogram


def show_histogram_image(image, save_path=None, channel=None):
    color_channels = analyse_color_channels(image)[1]
    histogram = create_histogram(image)
    image_count = 1
    color = ['red', 'green', 'blue']

    if color_channels == 1:
        color = ['black']
        channel = 0
    elif channel is None:
        image_count = 3

    if channel is None:

        result_histogram, axs = plt.subplots(1, len(histogram), figsize=(15, 5))
        color = ['red', 'green', 'blue']
        for i in range(len(histogram)):
            axs[i].bar(range(256), histogram[i], color=['red', 'green', 'blue'][i])
            axs[i].set_title(f'Channel {color[i]}')
            axs[i].set_xlabel('Pixel Value')
            axs[i].set_ylabel('Frequency')

            result_histogram.suptitle('RGB Histogram')
        if save_path is not None:
            result_histogram.savefig(f'{save_path}{i}.png')
        result_histogram.show()

    else:
        if channel > 2:
            print("Could not find color channel no. ", channel, " generating histogram of default color channel 0")
            channel = 0
        result_histogram = generate_single_channel_histogram(histogram[channel], color, channel)
        if save_path is not None:
            result_histogram.savefig(f'{save_path}.png')
        result_histogram.show()


def generate_single_channel_histogram(histogram, color, channel):
    plt.figure(figsize=(10, 6))
    plt.bar(range(256), histogram, color=color[channel])
    if color[0] == 'black':
        plt.title('Grayscale Image')
    else:
        plt.title(f'Channel {color[channel]}')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    return plt

