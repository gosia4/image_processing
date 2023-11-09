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


# nie kompiluje się!
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
            cubed_diff = ((i - mean_value[c]) ** 3) * histogram[c][i]
            sum_cubed_diff[c] += cubed_diff

    # Calculate the variance as the average of squared differences
    a_coefficient = []
    for c in range(color_channels):
        a_coefficient.append(0)
        a_coefficient[c] = (1 / (total_pixels * sd_value[c] ** 3)) * sum_cubed_diff[c]

    return a_coefficient


# Stopped working here. All above functions are optimized.


def asymmetry_coefficient_2(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = width * height
    histogram = sp.create_histogram(image)
    mean_value = mean_pixel_value(image)
    v = variance(image)

    third_deviation = []
    sum_cubed_diff = []
    for c in range(color_channels):
        sum_cubed_diff.append(0)
        third_deviation.append(0)
        third_deviation[c] = v[c] ** (3 / 2)
        for i in range(256):
            cubed_diff = ((i - mean_value[c]) ** 3) * histogram[c][i]
            sum_cubed_diff[c] += cubed_diff

    # Calculate the variance as the average of squared differences
    a_coefficient = []
    for c in range(color_channels):
        a_coefficient.append(0)
        a_coefficient[c] = sum_cubed_diff[c] / (third_deviation[c] * total_pixels)

    return a_coefficient

def flattening_coefficient(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = height * width
    histogram = sp.create_histogram(image)
    mean_value = mean_pixel_value(image)
    sd_value = standard_deviation(image)

    sum_fourth_diff = []
    for c in range(color_channels):
        sum_fourth_diff.append(0)
        # Iterate over pixel values (0 to 255)
        for i in range(256):
            forth_diff = ((i - mean_value[c]) ** 4) * histogram[c][i]
            sum_fourth_diff[c] += forth_diff

    f_coefficient = []
    for c in range(color_channels):
        f_coefficient.append(0)
        # Calculate the variance as the average of squared differences
        f_coefficient[c] = ((1 / (total_pixels * sd_value[c] ** 4)) * sum_fourth_diff[c]) - 3

    return f_coefficient

def flattening_coefficient_2(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = height * width
    histogram = sp.create_histogram(image)
    mean_value = mean_pixel_value(image)
    v = variance(image)

    fourth_deviation = []
    sum_fourth_diff = []
    for c in range(color_channels):
        sum_fourth_diff.append(0)
        fourth_deviation.append(0)
        fourth_deviation[c] = v[c] ** 2
        for i in range(256):
            cubed_diff = ((i - mean_value[c]) ** 3) * histogram[c][i]
            sum_fourth_diff[c] += cubed_diff

    # Calculate the variance as the average of squared differences
    f_coefficient = []
    for c in range(color_channels):
        f_coefficient.append(0)
        f_coefficient[c] = (sum_fourth_diff[c] / (fourth_deviation[c] * total_pixels)) - 3

    return f_coefficient


def variation_coefficient_ii(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels_squared = (width * height) ** 2
    histogram = sp.create_histogram(image)


    pixel_sum = []
    for c in range(color_channels):
        pixel_sum.append(0)
        for i in range(256):
            pixel_sum[c] += ((histogram[c][i]) ** 2)

    variant_ii = []
    for c in range(color_channels):
        variant_ii.append(0)
        variant_ii[c] = pixel_sum[c] / total_pixels_squared

    return variant_ii


def information_source_entropy(image):
    width, height = image.size
    color_channels = sp.analyse_color_channels(image)[1]
    total_pixels = width * height
    histogram = sp.create_histogram(image)

    pixel_sum = []
    for c in range(color_channels):
        pixel_sum.append(0)
        for i in range(256):
            if histogram[i] > 0:
                pixel_sum += (histogram[i] * math.log2((histogram[i])/total_pixels))

    ise = []
    for c in range(color_channels):
        ise.append(0)
        ise[c] = (-1) * pixel_sum[c] / total_pixels

    return ise
