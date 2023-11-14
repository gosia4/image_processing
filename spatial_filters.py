import support_functions as sp
from PIL import Image
from matplotlib import pyplot as plt
import math
import numpy as np

def uniform_histogram(image, min_brightness, max_brightness, output):
    if sp.analyse_color_channels(image)[1] == 1:
        width, height = image.size

        histogram = sp.calculate_histogram(image)

        total_pixels = 0

        for count in histogram:
            total_pixels += count

        # cumulative_histogram, sums of pixel counts for different intensity values
        cumulative_histogram = [0]

        for intensity in range(1, 256):  # Go from 1 to 255. Intensity.
            previous_cumulative = cumulative_histogram[-1]  # -1 refers to the last element in a list
            current_cumulative = previous_cumulative + histogram[
                intensity]  # we calcuate new brightness based on the histogram
            cumulative_histogram.append(current_cumulative)

        new_image = Image.new(image.mode, (width, height))  # new image for both gray scale and RGB scle

        for x in range(width):
            for y in range(height):
                old_brightness = image.getpixel((x, y))  # gets the current brightness level of the pixel
                new_brightness = cumulative_histogram[old_brightness] * (
                            max_brightness - min_brightness) / total_pixels  # function for new brightness
                new_image.putpixel((x, y), int(new_brightness + min_brightness))  # Update the pixel value.

        new_image.show()
        sp.save_image(new_image, output)
    else:
        uniform_histogram_color(image, min_brightness, max_brightness, output)


def uniform_histogram_color(image, min_brightness, max_brightness, output):
    width, height = image.size

    histogram_r = [0] * 256
    histogram_g = [0] * 256
    histogram_b = [0] * 256

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            histogram_r[r] += 1
            histogram_g[g] += 1
            histogram_b[b] += 1

    total_pixels = width * height

    cumulative_histogram_r = [0]
    cumulative_histogram_g = [0]
    cumulative_histogram_b = [0]

    cumulative_r = 0
    cumulative_g = 0
    cumulative_b = 0

    for i in range(256):
        cumulative_r += histogram_r[i]
        cumulative_histogram_r.append(cumulative_r)

        cumulative_g += histogram_g[i]
        cumulative_histogram_g.append(cumulative_g)

        cumulative_b += histogram_b[i]
        cumulative_histogram_b.append(cumulative_b)

    new_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))

            new_r = int(cumulative_histogram_r[r] * (max_brightness - min_brightness) / total_pixels + min_brightness)
            new_g = int(cumulative_histogram_g[g] * (max_brightness - min_brightness) / total_pixels + min_brightness)
            new_b = int(cumulative_histogram_b[b] * (max_brightness - min_brightness) / total_pixels + min_brightness)

            new_image.putpixel((x, y), (new_r, new_g, new_b))

    new_image.show()
    new_image.save(output)


def edge_sharpening(image, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("This program does not support this color model.")
        return

    # Define a Laplacian kernel for edge sharpening
    laplacian_kernel = [[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]]

    edge_values = 0
    for i in range(3):
        edge_values += laplacian_kernel[0][i]
    for j in range(3):
        edge_values += laplacian_kernel[j][0]

    for x in range(width):
        for y in range(height):
            new_pixel = [0] * color_channels
            border_pixels = 0

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j

                    if 0 <= target_y < height:
                        if 0 <= target_x < width:
                            pixel = image.getpixel((target_x, target_y))
                            if color_channels == 1:
                                new_pixel[0] += pixel * laplacian_kernel[i + 1][j + 1]

                            else:
                                for c in range(color_channels):
                                    new_pixel[c] += pixel[c] * laplacian_kernel[i + 1][j + 1]
                        else:
                            border_pixels += 1
                    else:
                        border_pixels += 1

            for b in range(border_pixels % 2):
                for c in range(color_channels):
                    new_pixel[c] -= int(new_pixel[c] / (2 - b))

            result_image.putpixel((x, y), tuple(new_pixel))

    sp.save_image(result_image, output)
    result_image.show()


def edge_sharpening_2(image, kernel, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("This program does not support this color model.")
        return

    kernel_size = len(kernel)
    kernel_radius = kernel_size // 2

    for x in range(width):
        for y in range(height):
            new_pixel = [0] * color_channels

            for i in range(-kernel_radius, kernel_radius + 1):
                for j in range(-kernel_radius, kernel_radius + 1):

                    target_x = x + i
                    target_y = y + j

                    if 0 <= target_x < width - 1:
                        if 0 <= target_y < height - 1:
                            pixel = image.getpixel((target_x, target_y))
                            if color_channels == 1:
                                new_pixel[0] += pixel * kernel[i + kernel_radius][j + kernel_radius]
                            else:
                                for c in range(color_channels):
                                    new_pixel[c] += pixel[c] * kernel[i + kernel_radius][j + kernel_radius]

            result_image.putpixel((x, y), tuple(new_pixel))

    sp.save_image(result_image, output)
    result_image.show()


def uolis_operator(image, output):
    width, height = image.size
    result_image, channels = sp.analyse_color_channels(image)

    if channels == 0:
        print("This program does not support this color model.")
        return

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            sample_arr = [] * channels

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j

                    if 0 <= target_x < width and 0 <= target_y < height:
                        if channels == 1:
                            sample_arr.append([image.getpixel((target_x, target_y))])
                        else:
                            sample_arr.append(list(image.getpixel((target_x, target_y))))

            a1 = sample_arr[1]
            a3 = sample_arr[5]
            a5 = sample_arr[7]
            a7 = sample_arr[3]
            x_nm = sample_arr[4]

            numerator = []
            denominator = []
            g_nm = []

            for c in range(channels):
                g_nm.append(0)
                numerator.append(0)
                denominator.append(0)
                numerator[c] = x_nm[c] ** 4
                denominator[c] = a1[c] * a3[c] * a5[c] * a7[c]
                if denominator[c] == 0:
                    g_nm[c] = 255
                elif numerator[c] <= 0:
                    g_nm[c] = 0
                else:
                    g_nm[c] = int(1/4 * math.log10(numerator[c] / denominator[c]))

            # print(g_nm)
            result_image.putpixel((x, y), tuple(g_nm))

    sp.save_image(result_image, output)
    result_image.show()

def uolis_operator_times_300(image, output):
    width, height = image.size
    result_image, channels = sp.analyse_color_channels(image)

    if channels == 0:
        print("This program does not support this color model.")
        return

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            sample_arr = [] * channels

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j

                    if 0 <= target_x < width and 0 <= target_y < height:
                        if channels == 1:
                            sample_arr.append([image.getpixel((target_x, target_y))])
                        else:
                            sample_arr.append(list(image.getpixel((target_x, target_y))))

            a1 = sample_arr[1]
            a3 = sample_arr[5]
            a5 = sample_arr[7]
            a7 = sample_arr[3]
            x_nm = sample_arr[4]

            numerator = []
            denominator = []
            g_nm = []

            for c in range(channels):
                g_nm.append(0)
                numerator.append(0)
                denominator.append(0)
                numerator[c] = x_nm[c] ** 4
                denominator[c] = a1[c] * a3[c] * a5[c] * a7[c]
                if denominator[c] == 0:
                    g_nm[c] = 255
                elif numerator[c] <= 0:
                    g_nm[c] = 0
                else:
                    g_nm[c] = int(300 * math.log10(numerator[c] / denominator[c]))

            # print(g_nm)
            result_image.putpixel((x, y), tuple(g_nm))

    sp.save_image(result_image, output)
    result_image.show()

def uolis_operator_no_log(image, output):
    width, height = image.size
    result_image, channels = sp.analyse_color_channels(image)

    if channels == 0:
        print("This program does not support this color model.")
        return

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            sample_arr = [] * channels

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j

                    if 0 <= target_x < width and 0 <= target_y < height:
                        if channels == 1:
                            sample_arr.append([image.getpixel((target_x, target_y))])
                        else:
                            sample_arr.append(list(image.getpixel((target_x, target_y))))

            a1 = sample_arr[1]
            a3 = sample_arr[5]
            a5 = sample_arr[7]
            a7 = sample_arr[3]
            x_nm = sample_arr[4]

            numerator = []
            denominator = []
            g_nm = []

            for c in range(channels):
                g_nm.append(0)
                numerator.append(0)
                denominator.append(0)
                numerator[c] = x_nm[c] ** 4
                denominator[c] = a1[c] * a3[c] * a5[c] * a7[c]
                if denominator[c] == 0:
                    g_nm[c] = 255
                elif numerator[c] <= 0:
                    g_nm[c] = 0
                else:
                    g_nm[c] = int(300 * (numerator[c] / denominator[c]))

            # print(g_nm)
            result_image.putpixel((x, y), tuple(g_nm))

    sp.save_image(result_image, output)
    result_image.show()
