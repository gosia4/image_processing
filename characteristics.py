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

        # Calculate the sum of pixel values
        for j in histogram:
            pixel_sum = 0
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


def variation_coefficient_i(image):
    color_channel = sp.analyse_color_channels(image)[1]
    mean_value = mean(image)
    sd_value = standard_deviation(image)
    if color_channel == 1:
        result = sd_value / mean_value
    elif color_channel == 3:
        result = [0, 0, 0]
        for i in range(color_channel):
            result[i] = sd_value[i] / mean_value[i]
    else:
        return
    return result


def asymmetry_coefficient(image):
    color_mode = sp.analyse_color_channels(image)[1]
    total_pixels = sp.total_pixels(image)
    histogram = sp.histogram(image)
    mean_value = mean(image)
    sd_value = standard_deviation(image)

    if color_mode == 1:

        sum_cubed_diff = 0

        # Iterate over pixel values (0 to 255)
        for i in range(256):
            cubed_diff = ((i - mean_value) ** 3) * histogram[i]
            sum_cubed_diff += cubed_diff

        # Calculate the variance as the average of squared differences
        a_coefficient = (1 / (total_pixels * sd_value ** 3)) * sum_cubed_diff

        return a_coefficient
    elif color_mode == 3:
        mean_values = mean(image)

        a_coefficient = [0, 0, 0]

        # Iterate over pixel values (0 to 255) and channels (R, G, B)
        for i in range(256):
            for j in range(3):
                cubed_diff = ((i - mean_values[j]) ** 3) * histogram[j][i]
                a_coefficient[j] += cubed_diff

        for i in range(len(a_coefficient)):  # len = 3
            a_coefficient[i] = (1 / (total_pixels * sd_value[i] ** 3)) * a_coefficient[i]

        return a_coefficient
    else:
        return


def flattening_coefficient(image):
    color_mode = sp.analyse_color_channels(image)[1]
    total_pixels = sp.total_pixels(image)
    histogram = sp.histogram(image)
    mean_value = mean(image)
    sd_value = standard_deviation(image)

    if color_mode == 1:

        sum_forth_diff = 0

        # Iterate over pixel values (0 to 255)
        for i in range(256):
            forth_diff = ((i - mean_value) ** 4) * histogram[i]
            sum_forth_diff += forth_diff

        # Calculate the variance as the average of squared differences
        f_coefficient = (1 / (total_pixels * sd_value ** 4)) * sum_forth_diff - 3

        return f_coefficient
    elif color_mode == 3:
        mean_values = mean(image)

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
    color_mode = sp.analyse_color_channels(image)[1]
    if color_mode == 1:
        total_pixels = width * height
        # Get the histogram
        histogram = sp.histogram(image)

        # Calculate the sum of pixel values
        pixel_sum = 0
        for i in range(256):
            pixel_sum += ((histogram[i]) ** 2)

        result = pixel_sum / (total_pixels ** 2)
        return result
    elif color_mode == 3:
        total_pixels = 3 * width * height
        result = []
        # Get the histogram
        histogram = sp.histogram(image)
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
    color_mode = sp.analyse_color_channels(image)[1]
    if color_mode == 1:
        total_pixels = width * height
        # Get the histogram
        histogram = sp.histogram(image)

        # Calculate the sum of pixel values
        pixel_sum = 0
        for i in range(256):
            if histogram[i] > 0:
                pixel_sum += (histogram[i] * math.log2((histogram[i])/total_pixels))

        result = (-1) * pixel_sum / total_pixels
        return result
    elif color_mode == 3:
        total_pixels = 3 * width * height
        result_array = []
        # Get the histogram
        histogram = sp.histogram(image)

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
