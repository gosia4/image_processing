import support_functions as sp
from PIL import Image


def mean(image):
    width, height = image.size
    color_mode = sp.analyse_color_channels(image)[1]
    if color_mode == 1:
        total_pixels = width * height
        # Get the histogram
        histogram = sp.histogram(image)

        # Calculate the sum of pixel values
        pixel_sum = 0
        for i in range(256):
            pixel_sum += i * histogram[i]
        mean_value = pixel_sum / total_pixels
        print(mean_value)
    elif color_mode == 3:
        total_pixels = 3 * width * height
        mean_values = []
        # Get the histogram
        histogram = sp.histogram(image)

        # Calculate the sum of pixel values
        for j in histogram:
            pixel_sum = 0
            for i in range(256):
                pixel_sum += i * j[i]
            mean_value = pixel_sum / total_pixels
            mean_values.append(mean_value)
        print(mean_values)
    else:
        return

