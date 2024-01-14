import cmath
import math
from scipy.fft import fft, ifft
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt



def bluestein_fft2(image, show_plot = False, logarithmic = False):
    rows, cols = image.size

    print("halo?")

    # Determine the size of the FFT along rows and columns
    m_rows = next_power_of_two(2 * rows - 1)
    m_cols = next_power_of_two(2 * cols - 1)

    # Generate the chirp functions for rows and columns
    omega_rows = np.exp(-2j * np.pi / m_rows)
    omega_cols = np.exp(-2j * np.pi / m_cols)

    twiddle_factors_rows = np.power(omega_rows, np.arange(rows))
    twiddle_factors_cols = np.power(omega_cols, np.arange(cols))

    # Pad the input image with zeros
    image_padded = np.zeros((m_rows, m_cols), dtype=image.dtype)
    image_padded[:rows, :cols] = image

    # Multiply the input image by the chirp functions along rows
    image_chirped_rows = np.zeros((m_rows, cols), dtype=complex)
    for i in range(m_rows):
        image_chirped_rows[i, :] = np.fft.ifft(np.fft.fft(image_padded[i, :]) * twiddle_factors_rows[i])

    # Multiply the result by the chirp functions along columns
    image_chirped_cols = np.zeros((m_rows, m_cols), dtype=complex)
    for j in range(m_cols):
        image_chirped_cols[:, j] = np.fft.ifft(np.fft.fft(image_chirped_rows[:, j]) * twiddle_factors_cols[j])

    # Trim the result to the original size
    result = np.real(image_chirped_cols[:rows, :cols])

    if show_plot:
        ft_spectrum = np.abs(result)
        shifted_spectrum = phase_shift(ft_spectrum)
        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
        plt.show()

    return result


def next_power_of_two(x):
    return 2 ** math.ceil(math.log2(x))

def cooley_tukey_fft(x):
    N = len(x)
    if N <= 1:
        return x
    even = cooley_tukey_fft(x[0::2])
    odd = cooley_tukey_fft(x[1::2])
    factor = [cmath.exp(-2j * math.pi * k / N) * odd[k] for k in range(len(odd))]
    return [even[k] + factor[k] for k in range(len(even))] + [even[k] - factor[k] for k in range(len(even))]


def ct_fft2(image, show_plot = False, logarithmic = False):
    image_array = np.array(image)

    if len(image_array.shape) > 2:
        image_array = np.mean(image_array, axis=-1)

    rows, cols = image_array.shape
    padded_rows = next_power_of_two(rows)
    padded_cols = next_power_of_two(cols)
    padded_image = np.zeros((padded_rows, padded_cols), dtype=image_array.dtype)
    padded_image[:rows, :cols] = image_array

    result = np.zeros((padded_rows, padded_cols), dtype=complex)

    for u in range(padded_rows):
        result[u, :] = cooley_tukey_fft(padded_image[u, :])

    for v in range(padded_cols):
        result[:, v] = cooley_tukey_fft(result[:, v])

    if show_plot:
        ft_spectrum = np.abs(result)
        shifted_spectrum = phase_shift(ft_spectrum)
        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
            plt.title('Cooley Tukey FFT (logarithmic)')
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
            plt.title('Cooley Tukey FFT (normal)')
        plt.show()

    return result


def phase_shift(arr):
    rows, cols = arr.shape
    mid_row, mid_col = rows // 2, cols // 2

    shifted_arr = np.empty_like(arr)

    for i in range(mid_row):
        for j in range(mid_col):
            shifted_arr[i, j] = arr[i + mid_row, j + mid_col]
            shifted_arr[i + mid_row, j + mid_col] = arr[i, j]
            shifted_arr[i, j + mid_col] = arr[i + mid_row, j]
            shifted_arr[i + mid_row, j] = arr[i, j + mid_col]

    return shifted_arr


def numpy_fft(image, show_plot = False, logarithmic = False):
    result = np.fft.fft2(image)

    if show_plot:
        ft_spectrum = np.abs(result)
        shifted_spectrum = phase_shift(ft_spectrum)
        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
            plt.title('Numpy lib FFT (logarithmic)')
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
            plt.title('Numpy lib FFT (normal)')
        plt.show()

