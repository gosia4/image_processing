import support_functions as sp
import math


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
        # print(mean_value)
        return mean_value
    elif color_mode == 3:
        total_pixels = 3 * width * height
        mean_values = []
        # Get the histogram
        histogram = sp.histogram(image)
        pixel_sum = 0
        # Calculate the sum of pixel values
        for j in histogram:

            for i in range(256):
                pixel_sum += i * j[i]
            mean_value = pixel_sum / total_pixels
            mean_values.append(mean_value)
        # print(mean_values)
        return mean_values
    else:
        return


def variance(image):
    color_mode = sp.analyse_color_channels(image)[1]
    total_pixels = sp.total_pixels(image)
    histogram = sp.histogram(image)

    if color_mode == 1:
        mean_value = mean(image)
        sum_squared_diff = 0

        # Iterate over pixel values (0 to 255)
        for i in range(256):
            squared_diff = ((i - mean_value) ** 2) * histogram[i]
            sum_squared_diff += squared_diff

        # Calculate the variance as the average of squared differences
        variance_value = (1 / total_pixels) * sum_squared_diff

        return variance_value
    elif color_mode == 3:
        mean_values = mean(image)

        variances = [0, 0, 0]

        # Iterate over pixel values (0 to 255) and channels (R, G, B)
        for i in range(256):
            for j in range(3):
                squared_diff = ((i - mean_values[j]) ** 2) * histogram[j][i]
                variances[j] += squared_diff

        for i in range(len(variances)):  # len = 3
            variances[i] /= total_pixels

        return variances
    else:
        return


def standard_deviation(image):
    variance_value = variance(image)
    color_channel = sp.analyse_color_channels(image)[1]
    if color_channel == 1:
        result = math.sqrt(variance_value)
    elif color_channel == 3:
        result = [0, 0, 0]
        for i in range(color_channel):
            result[i] = math.sqrt(variance_value[i])
    else:
        return
    return result
