import support_functions as sp
from PIL import Image
from matplotlib import pyplot as plt
import math
import numpy as np


def uniform_histogram(image, min_brightness, max_brightness, output):
    result_image, color_channels = sp.analyse_color_channels(image)
    width, height = image.size

    # histogram = sp.calculate_histogram(image)
    histogram = sp.create_histogram(image)

    total_pixels = width * height

    # cumulative_histogram, sums of pixel counts for different intensity values
    cumulative_histogram = [[0] for c in range(color_channels)]
    cumulative_val = [0 for c in range(color_channels)]

    for i in range(256):
        for c in range(color_channels):
            cumulative_val[c] += histogram[c][i]
            cumulative_histogram[c].append(cumulative_val[c])


    for x in range(width):
        for y in range(height):
            intensity = sp.int_or_tuple_to_list(image.getpixel((x, y)))
            new_intensity = []
            for c in range(color_channels):
                new_intensity.append(int(cumulative_histogram[c][intensity[c]] * (max_brightness - min_brightness) / total_pixels + min_brightness))

            result_image.putpixel((x, y), tuple(new_intensity))

    result_image.show()
    result_image.save(output)


def edge_sharpening(image, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    # laplacian_kernel = [[0, -1, 0],
    #                     [-1, 5, -1],
    #                     [0, -1, 0]]
    for x in range(width):
        result_image.putpixel((x,0), image.getpixel((x,0)))
        result_image.putpixel((x,height-1), image.getpixel((x,height-1)))
    for y in range(height):
        result_image.putpixel((0, y), image.getpixel((0, y)))
        result_image.putpixel((width-1, y), image.getpixel((width-1, y)))


    if color_channels == 1:
        for x in range(1, width - 1):
            for y in range(1, height - 1):

                result_image.putpixel((x, y), tuple(image.getpixel((x - 1, y)) -
                                                    image.getpixel((x, y - 1)) -
                                                    image.getpixel((x + 1, y)) -
                                                    image.getpixel((x, y + 1)) +
                                                    image.getpixel((x, y)) * 5))

    else:
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                new_pixel = [0, 0, 0]

                for c in range(color_channels):
                    new_pixel[c] = (-image.getpixel((x-1, y))[c] -
                                    image.getpixel((x, y-1))[c] -
                                    image.getpixel((x+1, y))[c] -
                                    image.getpixel((x, y+1))[c] +
                                    image.getpixel((x, y))[c] * 5)

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
                    g_nm[c] = int((numerator[c] / denominator[c]))

            # print(g_nm)
            result_image.putpixel((x, y), tuple(g_nm))

    sp.save_image(result_image, output)
    result_image.show()
