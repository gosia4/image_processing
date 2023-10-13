import support_functions
import numpy as np
from PIL import Image


def mse(image1, image2):
    if image1.size != image2.size:
        print("Images must have the same dimensions.")
    else:
        img1 = np.array(image1)
        img2 = np.array(image2)
        # Kwadrat różnicy elementów
        squared_diff = np.square(img1.astype(float) - img2.astype(float))

        # Suma tych kwadratów
        sum_squared_diff = np.sum(squared_diff)

        # Calculate the mean squared error
        mse_value = sum_squared_diff / (img1.shape[0] * img1.shape[1])
        print(mse_value)


def pmse(image1, image2):
    if image1.size != image2.size:
        print("Images must have the same dimensions.")
    else:
        img1 = np.array(image1)
        img2 = np.array(image2)
        # Kwadrat różnicy elementów
        squared_diff = np.square(img1.astype(float) - img2.astype(float))
        max_value = np.max(img1.astype(float))
        temp = squared_diff / (max_value ** 2)
        # Suma tych kwadratów
        sum_squared_diff = np.sum(temp)
        pmse_value = sum_squared_diff / (img1.shape[0] * img1.shape[1])
        print(pmse_value)


def pmse2(image1, image2):
    if image1.size != image2.size:
        print("Images must have the same dimensions.")
    else:
        img1 = np.array(image1)
        img2 = np.array(image2)
        # Kwadrat różnicy elementów
        squared_diff = np.square(img1.astype(float) - img2.astype(float))

        # Suma tych kwadratów
        sum_squared_diff = np.sum(squared_diff)

        # Calculate the mean squared error
        mse_value = sum_squared_diff / (img1.shape[0] * img1.shape[1])

        # Calculate the peak mean square error (PMSE)
        pmse_value = np.max(mse_value)
        print(pmse_value)



