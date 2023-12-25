import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def one_dimensional_dft(data):  # 1d fourier transform
    size = len(data)
    sample_arr = np.arange(size)  # an array where the index numbers of the elements in the data is stored
    result = np.zeros(size, dtype=np.complex128)  # create a numpy array with zeros, where complex numbers can be

    for k in range(size):
        result[k] = np.sum(data * np.exp(-2j * np.pi * sample_arr * k / size))

    return result


def dft_row(image):
    # height, width = image.size
    dft_rows = np.zeros_like(image, dtype=np.complex128)  # with zeros, size is the size of the image

    image_array = np.transpose(np.array(image))
    height = len(image_array[0])
    for row in range(height):
        row_data = image_array[row]
        dft_rows[row] = one_dimensional_dft(row_data)

    return dft_rows


def dft_column(image):
    # height, width = image.size

    image_array = np.transpose(np.array(image))
    width = len(image_array)
    height = len(image_array[0])
    dft_columns = np.zeros_like(image, dtype=np.complex128)

    for column in range(width):
        column_data = image_array[column]
        dft_columns[column] = one_dimensional_dft([column_data])

    return dft_columns

def dft2d(image):
    return dft_column(dft_row(image))


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


def plot_fourier_transform(image):
    fourier_transform = dft2d(image)
    shifted_transform = phase_shift(fourier_transform)
    magnitude_spectrum = np.log(np.abs(shifted_transform) + 1)

    plt.subplot(1, 1, 1)
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Amplituda Transformaty Fouriera')
    plt.colorbar()

    plt.show()


def discrete_fourier_transform_2d(image, show_plot=False, logarithmic=False):
    # Assuming 'image' is a 2D array (image data)
    image_array = np.array(image)
    M, N = image_array.shape
    result = np.zeros((M, N), dtype=np.complex128)

    for u in range(M):
        for v in range(N):
            sum_val = 0
            for x in range(M):
                for y in range(N):
                    pixel_value = image_array[x, y]
                    angle = -2 * np.pi * ((u * x) / M + (v * y) / N)
                    sum_val += pixel_value * (np.cos(angle) + 1j * np.sin(angle))
            result[u, v] = sum_val

    if show_plot:
        ft_spectrum = np.abs(result)
        shifted_spectrum = phase_shift(ft_spectrum)
        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
        plt.show()

    return result

def inverse_fourier_transform_2d(frequency, show_image=False):
    M, N = frequency.shape
    result = np.zeros((M, N), dtype=np.complex128)

    for x in range(M):
        for y in range(N):
            pixel_value = 0
            for u in range(M):
                for v in range(N):
                    value = frequency[u, v]
                    angle = 2 * np.pi * ((u * x) / M + (v * y) / N)
                    pixel_value += value * (np.cos(angle) - 1j * np.sin(angle))
            result[x, y] = pixel_value / (M * N)

    if show_image:
        image = Image.fromarray((result * 255).astype(np.uint8))
        image.show()

        # Ff the number of pixels is even then the image will be shifted 1 pixel to the right and bottom
        # To counteract this maybe manually shift the image
        # this is probably caused during the phase shift

    return result


def fft(x):
    N = len(x)

    if N <= 1:
        return x

    # divide into even and odd elements
    even = fft(x[0::2])
    odd = fft(x[1::2])

    # initialize with zeros
    result = [0] * N

    for k in range(N // 2):
        # twiddle factor, before adding or subtracting results of the fft for even elements
        T = np.exp(-2j * np.pi * k / N) * odd[k]
        result[k] = even[k] + T
        result[k + N // 2] = even[k] - T

    return result


def fft2d(image, output=None):
    # transpose to be sure that rows and columns are properly calculated
    transposed_image = np.transpose(image)

    # Apply FFT along rows
    fft_rows = []
    for row in transposed_image:
        fft_rows.append(fft(row))
    fft_rows = np.array(fft_rows)

    # Transpose the result (because rows have now shifted phase) and apply FFT for columns
    fft_cols = []
    for col in np.transpose(fft_rows):
        fft_cols.append(fft(col))
    fft_cols = np.array(fft_cols)

    if output:
        plt.imsave(output, np.abs(fft_cols), cmap='gray')

    return fft_cols

# def visualize_spectrum(image_fft):
#     spectrum = np.log(np.abs(image_fft) + 1)
#     shifted_spectrum = phase_shift(spectrum)
#
#     plt.imshow(shifted_spectrum, cmap='gray')
#     plt.title("Fourier Spectrum")
#     plt.show()


def visualize_image(image_fft):
    # without logarithmic function there is only one dot in the middle
    image_magnitude = np.abs(image_fft)
    shifted_image = phase_shift(image_magnitude)

    plt.subplot(1, 2, 1)
    plt.imshow(shifted_image, cmap='gray')
    plt.title("Image after FFT without log function")
    # plt.show()

    spectrum = np.log(np.abs(image_fft) + 1)
    shifted_spectrum = phase_shift(spectrum)
    plt.subplot(1, 2, 2)
    plt.imshow(shifted_spectrum, cmap='gray')
    plt.title("Fourier Spectrum")
    plt.show()



def ifft(x):
    N = len(x)

    if N <= 1:
        return x

    # divide into even and odd elements
    even = ifft(x[0::2])
    odd = ifft(x[1::2])

    # initialize with zeros
    result = [0] * N

    for k in range(N // 2):
        # twiddle factor, before adding or subtracting results of the ifft for even elements
        # like in the fft, but 2j instead of -2j
        T = np.exp(2j * np.pi * k / N) * odd[k]
        result[k] = even[k] + T
        result[k + N // 2] = even[k] - T

    return result


def ifft2d(image_fft, output=None, show=True):
    # Transpose the image to ensure proper calculation of rows and columns
    transposed_image_fft = np.transpose(image_fft)

    # Apply ifft along rows
    ifft_rows = []
    for row in transposed_image_fft:
        ifft_rows.append(ifft(row))
    ifft_rows = np.array(ifft_rows)

    # Transpose the result and apply ifft along columns
    ifft_cols = []
    for col in np.transpose(ifft_rows):
        ifft_cols.append(ifft(col))
    ifft_cols = np.array(ifft_cols)

    if output:
        plt.imsave(output, np.abs(ifft_cols), cmap='gray')
    if show:
        plt.imshow(np.abs(ifft_cols), cmap='gray')
        plt.title("Reconstructed Image")
        plt.show()

    return ifft_cols


#  visualize image after inverse fourier transform

# def visualize_image_ifft(image_ifft):
#     plt.imshow(np.abs(image_ifft), cmap='gray')
#     plt.title("Reconstructed Image")
#     plt.show()

    # Normalize the image to the range [0, 255] for display, otherwise it is an error with converting to float
    # image_ifft_display = np.abs(image_ifft) * 255 / np.max(np.abs(image_ifft))

    # plt.imshow(image_ifft_display, cmap='gray')
    # plt.title("Image after Inverse Fourier Transform")
    # plt.show()

