import support_functions
import numpy as np
import math
from PIL import Image


def mse(image1, image2):
    if image1.size != image2.size:
        print("Images must have the same dimensions.")
        return "Error"
    else:
        img1 = np.array(image1)
        img2 = np.array(image2)
        width, height = image1.size
        # Kwadrat różnicy elementów i ich suma
        sum_squared_diff = 0
        squared_diff = np.zeros((width, height))
        for i in range(width):
            for j in range(height):
                squared_diff[i, j] = (img1[i, j].astype(float) - img2[i, j].astype(
                    float)) ** 2  # konwertuje pixele na float
                sum_squared_diff += squared_diff[i, j]

        # Calculate the mean squared error
        mse_value = sum_squared_diff / (width * height)
        return mse_value


def pmse(image1, image2):
    mse_value = mse(image1, image2)
    img1 = np.array(image1)
    width, height = image1.size

    max_squared_value = 0
    for i in range(width):
        for j in range(height):
            if img1[i][j] > max_squared_value:
                max_squared_value = img1[i][j]

    pmse_value = mse_value / (max_squared_value ** 2)
    return pmse_value


def snr(image1, image2):
    img1 = np.array(image1)
    img2 = np.array(image2)
    width, height = image1.size
    # Calculate the sum of squared differences
    sum_squared_diff = 0
    sum_squared_signal = 0

    for i in range(width):
        for j in range(height):
            squared_diff = (img1[i, j].astype(float) - img2[i, j].astype(float)) ** 2
            sum_squared_diff += squared_diff
            sum_squared_signal += (img1[i, j].astype(float) ** 2)

    # wersja 1
    # # Kwadrat różnicy elementów
    # squared_diff = (img1.astype(float) - img2.astype(float)) ** 2
    #
    # # Suma tych kwadratów
    # sum_squared_diff = 0
    # for i in range(width):
    #     for j in range(height):
    #         sum_squared_diff += squared_diff[i, j]

    if sum_squared_diff == 0:
        snr_value = float('inf')  # Set SNR to infinity for zero noise
    else:
        snr_value = 10 * np.log10(sum_squared_signal / sum_squared_diff)
    return snr_value


def psnr(image1, image2):
    img1 = np.array(image1)
    img2 = np.array(image2)
    width, height = image1.size
    sum_squared_diff = 0
    max_value = 0
    for i in range(width):
        for j in range(height):
            if img1[i][j] > max_value:
                max_value = img1[i][j]
                squared_diff = (img1[i, j].astype(float) - img2[i, j].astype(float)) ** 2
                sum_squared_diff += squared_diff
    max_squared_value = max_value ** 2
    if sum_squared_diff == 0:
        psnr_value = float('inf')  # Set SNR to infinity for zero noise
    else:
        psnr_value = 10 * np.log10(max_squared_value / sum_squared_diff)
    return psnr_value

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
