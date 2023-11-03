import support_functions as sp
import math


def mean_pixel_value(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = width * height

    # Get the histogram
    histogram = sp.create_histogram(image)

    # Calculate the sum of pixel values
    pixel_sum = []
    for c in range(color_channels):
        pixel_sum.append(0)
        for i in range(256):
            pixel_sum[c] += i * histogram[c][i]

    mean_value = []
    for c in range(color_channels):
        mean_value.append(0)
        mean_value[c] = pixel_sum[c] / total_pixels

    return mean_value


def variance(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = width * height
    histogram = sp.create_histogram(image)

    mean_value = mean_pixel_value(image)

    sum_squared_diff = []
    for c in range(color_channels):
        sum_squared_diff.append(0)
        for i in range(256):
            squared_diff = ((i - mean_value[c]) ** 2) * histogram[c][i]
            sum_squared_diff[c] += squared_diff

    # Calculate the variance as the average of squared differences
    variance_value = []
    for c in range(color_channels):
        variance_value.append(0)
        variance_value[c] = sum_squared_diff[c] / total_pixels

    return variance_value


def standard_deviation(image):
    variance_value = variance(image)
    color_channel = sp.analyse_color_channels(image)[1]
    standard_deviation_value = []

    for c in range(color_channel):
        standard_deviation_value.append(0)
        standard_deviation_value[c] = math.sqrt(variance_value[c])

    return standard_deviation_value


def variation_coefficient_i(image):
    color_channel = sp.analyse_color_channels(image)[1]
    mean_value = mean_pixel_value(image)
    sd_value = standard_deviation(image)

    for c in range(color_channel):
        vc_i_value = []
        vc_i_value[c] = sd_value[c] / mean_value[c]

    return vc_i_value



# def asymmetry_coefficient_2(image):
#     width, height = image.size
#     color_channels = sp.analyse_color_channels(image)[1]
#     total_pixels = width * height * color_channels
#     histogram = sp.create_histogram(image)
#     mean_value = mean_pixel_value(image)
#     sd_value = standard_deviation(image)
#
#     sum_cubed_diff = []
#         for c in range(color_channels):
#             sum_cubed_diff.append(0)
#             for i in range(256):
#                 cubed_diff = ((i - mean_value[c]) ** 2) * histogram[c][i]
#                 sum_cubed_diff[c] += cubed_diff
#
#         variance3_value = []
#         for c in range(color_channels):
#             variance3_value.append(0)
#             variance3_value[c] = sum_cubed_diff[c] / total_pixels

def asymmetry_coefficient(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = width * height
    histogram = sp.create_histogram(image)
    mean_value = mean_pixel_value(image)
    sd_value = standard_deviation(image)

    sum_cubed_diff = []
    for c in range(color_channels):
        sum_cubed_diff.append(0)
        for i in range(256):
            cubed_diff = ((i - mean_value[c]) ** 3) * histogram[i]
            sum_cubed_diff[c] += cubed_diff

    # Calculate the variance as the average of squared differences
    a_coefficient = []
    for c in range(color_channels):
        a_coefficient.append(0)
        a_coefficient[c] = (1 / (total_pixels * sd_value[c] ** 3)) * sum_cubed_diff[c]

    return a_coefficient


# Stopped working here. All above functions are optimized.


def flattening_coefficient(image):
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = sp.total_pixels(image)
    histogram = sp.create_histogram(image)
    mean_value = mean_pixel_value(image)
    sd_value = standard_deviation(image)

    if color_channels == 1:

        sum_forth_diff = 0

        # Iterate over pixel values (0 to 255)
        for i in range(256):
            forth_diff = ((i - mean_value) ** 4) * histogram[i]
            sum_forth_diff += forth_diff

        # Calculate the variance as the average of squared differences
        f_coefficient = (1 / (total_pixels * sd_value ** 4)) * sum_forth_diff - 3

        return f_coefficient
    elif color_channels == 3:
        mean_values = mean_pixel_value(image)

        f_coefficient = [0, 0, 0]

        # Iterate over pixel values (0 to 255) and channels (R, G, B)
        for i in range(256):
            for j in range(3):
                forth_diff = ((i - mean_values[j]) ** 4) * histogram[j][i]
                f_coefficient[j] += forth_diff

        for i in range(len(f_coefficient)):  # len = 3
            f_coefficient[i] = (1 / (total_pixels * sd_value[i] ** 4)) * f_coefficient[i] - 3

        return f_coefficient
    else:
        return


def variation_coefficient_ii(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    if color_channels == 1:
        total_pixels = width * height
        # Get the histogram
        histogram = sp.create_histogram(image)

        # Calculate the sum of pixel values
        pixel_sum = 0
        for i in range(256):
            pixel_sum += ((histogram[i]) ** 2)

        result = pixel_sum / (total_pixels ** 2)
        return result
    elif color_channels == 3:
        total_pixels = 3 * width * height
        result = []
        # Get the histogram
        histogram = sp.create_histogram(image)
        # Calculate the sum of pixel values
        for j in histogram:
            pixel_sum = 0
            for i in range(256):
                pixel_sum += ((j[i]) ** 2)
            before_result = pixel_sum / (total_pixels ** 2)
            result.append(before_result)

        return result
    else:
        return


def information_source_entropy(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    if color_channels == 1:
        total_pixels = width * height
        # Get the histogram
        histogram = sp.create_histogram(image)

        # Calculate the sum of pixel values
        pixel_sum = 0
        for i in range(256):
            if histogram[i] > 0:
                pixel_sum += (histogram[i] * math.log2((histogram[i])/total_pixels))

        result = (-1) * pixel_sum / total_pixels
        return result
    elif color_channels == 3:
        total_pixels = 3 * width * height
        result_array = []
        # Get the histogram
        histogram = sp.create_histogram(image)

        # Calculate the sum of pixel values
        for j in histogram:
            pixel_sum = 0
            for i in range(256):
                if j[i] > 0:
                    pixel_sum += (j[i] * math.log2(j[i] / total_pixels))

            result = (-1) * pixel_sum / total_pixels
            result_array.append(result)
        return result_array
    else:
        return
