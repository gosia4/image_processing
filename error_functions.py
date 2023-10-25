import numpy as np
import support_functions as sp


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
                sum_squared_diff += ((img1[i, j].astype(int) - img2[i, j].astype(int)) ** 2)

        return sum_squared_diff
def mse(image1, image2):
    ssd = squared_sum_diff(image1, image2)
    width, height = image1.size
    if np.any(ssd == "Error"):
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
                old_value = sp.process_int_or_tuple(image1.getpixel((x, y)))
                new_value = sp.process_int_or_tuple(image2.getpixel((x, y)))
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

    if color_channels_1 * color_channels_2 == 1:
        if ssd != 0:
            snr_value = 10 * np.log10(sum_squared_signal / ssd)

    elif np.any(ssd == 0):
        for i in range(3):
            if ssd[i] == 0:
                snr_value[i] = float('inf')
            elif color_channels_1 == 1:
                snr_value[i] = 10 * np.log10(sum_squared_signal / ssd[i])
            else:
                snr_value[i] = 10 * np.log10(sum_squared_signal[i] / ssd[i])

    else:
        snr_value = 10 * np.log10(sum_squared_signal / ssd)
    return snr_value


def psnr(image1, image2):
    ssd = squared_sum_diff(image1, image2)

    color_channels_1 = sp.analyse_color_channels(image1)[1]
    color_channels_2 = sp.analyse_color_channels(image2)[1]

    width, height = image1.size
    max = 65025 * width * height

    psnr_value = ([0, 0, 0])

    if color_channels_1 * color_channels_2 == 1:
        if ssd != 0:
            return 10 * np.log10(max / ssd)

    elif np.any(ssd == 0):
        for i in range(3):
            if ssd[i] == 0:
                psnr_value[i] = float('inf')
            else:
                psnr_value[i] = 10 * np.log10(max / ssd[i])

    else:
        snr_value = 10 * np.log10(np.array([max, max, max]) / ssd)

    return snr_value


def md(image1, image2):
    img1 = np.array(image1).astype(int)
    img2 = np.array(image2).astype(int)

    color_channels_1 = sp.analyse_color_channels(image1)[1]
    color_channels_2 = sp.analyse_color_channels(image2)[1]

    channels = color_channels_2 * color_channels_1
    if channels > 3:
        channels = 3

    width, height = image1.size


    if channels == 1:
        max_diff = 0
    else:
        max_diff = [0, 0, 0]

    for i in range(width):
        for j in range(height):
            diff = img1[i][j] - img2[i][j]
            if channels == 1:
                if abs(diff) > max_diff:
                    max_diff = abs(diff)
            else:
                for c in range(channels):
                    if abs(diff[c]) > max_diff[c]:
                        max_diff[c] = abs(diff[c])

    return max_diff
