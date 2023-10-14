import support_functions
import numpy as np
from PIL import Image


def mse(image1, image2):
    if image1.size != image2.size:
        print("Images must have the same dimensions.")
        return "Error"
    else:
        img1 = np.array(image1)
        img2 = np.array(image2)
        width, height = image1.size
        # Kwadrat różnicy elementów
        # squared_diff = np.square(img1.astype(float) - img2.astype(float))
        squared_diff = (img1.astype(float) - img2.astype(float)) ** 2

        # Suma tych kwadratów
        sum_squared_diff = 0
        for i in range(width):
            for j in range(height):
                sum_squared_diff += squared_diff[i, j]

        # Calculate the mean squared error
        mse_value = sum_squared_diff / (width * height)
        #print(mse_value)
        return mse_value


def pmse(image1, image2):
    mse_value = mse(image1, image2)
    img1 = np.array(image1)
    width, height = image1.size
    # Calculate the maximum value of (img1.astype(float) ** 2)

    max_squared_value = 0
    for i in range(width):
        for j in range(height):
            if img1[i][j] > max_squared_value:
                max_squared_value = img1[i][j]
    # max_squared_value = calculate_max(img1.astype(float) ** 2)

    pmse_value = mse_value / max_squared_value
    #print(pmse_value)
    return pmse_value

# def snr(image1, image2):
