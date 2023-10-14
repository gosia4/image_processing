import support_functions
import numpy as np
import math
import support_functions as sp
from PIL import Image


def squared_sum_diff(image1, image2):
    if image1.size != image2.size:
        print("Images must have the same dimensions.")
        return "Error"
    else:
        img1 = np.array(image1)
        img2 = np.array(image2)
        width, height = image1.size
        sum_squared_diff = 0
        for i in range(width):
            for j in range(height):
                sum_squared_diff += (img1[i, j].astype(int) - img2[i, j].astype(int)) ** 2

        return sum_squared_diff
def mse(image1, image2):
    ssd = squared_sum_diff(image1, image2)
    width, height = image1.size
    if ssd == "Error":
        return
    mse_value = ssd / (width * height)
    return mse_value

def mse_no_numpy(image1, image2):
    if image1.size != image2.size:
        print("Can not compare images of different dimensions")
        return
    else:

        width, height = image1.size
        color_channels = sp.analyse_color_channels(image1)[1]
        sum_squared_diff = 0
        for x in range(width):
            for y in range(height):
                old_value = sp.int_or_tuple_to_array(image1.getpixel((x, y)))
                new_value = sp.int_or_tuple_to_array(image2.getpixel((x, y)))
                sum_squared_diff += (old_value - new_value) ** 2
        # Calculate the mean squared error
        mse_value = sum_squared_diff / (width * height)
        return mse_value


def pmse(image1, image2):
    mse_value = mse(image1, image2)
    pmse_value = mse_value / np.array([65025, 65025, 65025])
    return pmse_value

def snr(image1, image2):
    img1 = np.array(image1)
    width, height = image1.size

    color_channels_1 = sp.analyse_color_channels(image1)[1]
    color_channels_2 = sp.analyse_color_channels(image2)[1]

    ssd = squared_sum_diff(image1, image2)
    sum_squared_signal = 0
    snr_value = np.array([0, 0, 0])

    for i in range(width):
        for j in range(height):
            sum_squared_signal += img1[i, j].astype(float) ** 2
    # wersja 1
    # # Kwadrat różnicy elementów
    # squared_diff = (img1.astype(float) - img2.astype(float)) ** 2

    # # Suma tych kwadratów
    # sum_squared_diff = 0
    # for i in range(width):
    #     for j in range(height):
    #         sum_squared_diff += squared_diff[i, j]

    if color_channels_1 * color_channels_2 == 1:
        if ssd != 0:
            snr_value = 10 * np.log10(sum_squared_signal / ssd)

    elif np.any(ssd == 0):
        for i in range(3):
            if ssd[i] != 0:
                snr_value[i] = float('inf')
            elif color_channels_1 == 1:
                snr_value[i] = 10 * np.log10(sum_squared_signal / ssd[i])
            else:
                snr_value[i] = 10 * np.log10(sum_squared_signal[i] / ssd[i])

    else:
        snr_value = 10 * np.log10(sum_squared_signal / ssd)
    return snr_value


# def snr2(image1, image2):
#     width, height = image1.size
#     mse_value = mse(image1, image2)
#     sum_squared = 0
#     sum_squared_signal = np.array([0, 0, 0])
#     for x in range(width):
#         for y in range(height):
#             sum_squared += sp.int_or_tuple_to_array(image1.getpixel((x, y)))
#
#     if np.any(mse_value == 0):
#         for i in range(3):
#             sum_squared_signal[i] = sum_squared[i] / mse_value[i]
#
#     else:
#         sum_squared_signal = sum_squared / mse_value
#
#     snr_value = 10 * np.log10(sum_squared_signal)
#     return snr_value
#
# def snr3(image1, image2):
#     img1 = np.array(image1)
#     img2 = np.array(image2)
#     width, height = image1.size
#     # Calculate the sum of squared differences
#     sum_squared_diff = 0
#     sum_squared_signal = 0
#
#     for i in range(width):
#         for j in range(height):
#             squared_diff = (img1[i, j].astype(int) - img2[i, j].astype(int)) ** 2
#             sum_squared_diff += squared_diff
#             sum_squared_signal += (img1[i, j].astype(float) ** 2)
#
#     # wersja 1
#     # # Kwadrat różnicy elementów
#     # squared_diff = (img1.astype(float) - img2.astype(float)) ** 2
#     #
#     # # Suma tych kwadratów
#     # sum_squared_diff = 0
#     # for i in range(width):
#     #     for j in range(height):
#     #         sum_squared_diff += squared_diff[i, j]
#
#     if sum_squared_diff == 0:
#         snr_value = float('inf')  # Set SNR to infinity for zero noise
#     else:
#         snr_value = 10 * np.log10(sum_squared_signal / sum_squared_diff)
#     return snr_value

def psnr(image1, image2):
    img1 = np.array(image1)
    img2 = np.array(image2)
    width, height = image1.size
    ssd = squared_sum_diff(image1, image2)

    #make checks for 0
    
    return 10 * np.log10(np.array([65025, 65025, 65025]) / ssd)

    #
    # sum_squared_diff = 0
    # sum_max_squared_signal = 0
    # max_value = 0
    #
    # for i in range(width):
    #     for j in range(height):
    #         squared_diff = (img1[i, j].astype(float) - img2[i, j].astype(float)) ** 2
    #         sum_squared_diff += squared_diff
    #         if img1[i, j].astype(float) > max_value:
    #             max_squared_value = max_value ** 2
    #             # sum_max_squared_signal += (img1[i, j].astype(float) ** 2)

    #
    # sum1 = 0
    # for i in range(width):
    #     for j in range(height):
    #         sum1 += max_squared_value[i][j]


def md(image1, image2):
    img1 = np.array(image1)
    img2 = np.array(image2)
    width, height = image1.size

    diff = 0
    max_diff = 0
    for i in range(width):
        for j in range(height):
            if img1[i][j] > img2[i][j]:
                diff = img1[i][j] - img2[i][j]
            else:
                diff = img2[i][j] - img1[i][j]
            if diff > max_diff:
                max_diff = diff

    return max_diff


# to raczej do usunięcia
def psnr5(img1, img2):
    image1 = np.array(img1)
    image2 = np.array(img2)
    width, height = img1.size
    max_value = float('-inf')  # Initialize max_value to negative infinity

    # Calculate sum of squared differences and find max value
    sum_squared_diff = 0
    for i in range(width):
        for j in range(height):
            if image1[i][j] > image2[i][j]:
                squared_diff = (image1[i][j] - image2[i][j]) ** 2
            else:
                squared_diff = (image2[i][j] - image1[i][j]) ** 2
            sum_squared_diff += squared_diff
            if image1[i][j] > max_value:
                max_value = image1[i][j]

    # Calculate psnr
    if sum_squared_diff == 0:
        psnr_value = float('inf')  # Set psnr to infinity for zero noise
    else:
        max_squared_value = max_value ** 2
        psnr_value = 10 * math.log10(max_squared_value / (sum_squared_diff / (width * height)))

    return psnr_value
