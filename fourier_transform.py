import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


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

    plt.axis('off')
    if show_plot:
        ft_spectrum = np.abs(result)
        shifted_spectrum = phase_shift(ft_spectrum)
        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
            plt.title('Custom, Slow FFT (logarithmic)')
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
            plt.title('Custom, Slow FFT (logarithmic)')
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

    # # divide into even and odd elements
    # even = fft(x[0::2])
    # odd = fft(x[1::2])
    # to store the number of even and odd indices
    even_indices = []
    for i in range(0, N, 2):  # from 0 to N, every 2 element
        even_indices.append(i)

    odd_indices = []
    for i in range(1, N, 2):  # from 1 to N, every 2 element
        odd_indices.append(i)

    # to store values of even and odd indices
    even_values = []
    for i in even_indices:
        even_values.append(x[i])

    odd_values = []
    for i in odd_indices:
        odd_values.append(x[i])

    even = fft(even_values)
    odd = fft(odd_values)

    # initialize with zeros
    result = [0] * N

    for k in range(N // 2):
        # twiddle factor, before adding or subtracting results of the fft for even elements
        # factor to rotate values from the spatial domain to the frequency domain
        T = np.exp(-2j * np.pi * k / N) * odd[k]
        result[k] = even[k] + T  # adding T for the even element
        result[k + N // 2] = even[k] - T  # subtracting T in the second part of the list

    return result


def fft2d(image, output=None, show_plot=False, logarithmic=False):
    # transpose to be sure that rows and columns are properly calculated
    transposed_image = np.transpose(image)

    # Apply FFT along rows
    fft_rows = []
    for row in transposed_image:
        fft_rows.append(fft(row))
    fft_rows = np.array(fft_rows)

    # Transpose the result (because rows have now shifted phase) and apply FFT for columns
    fft_cols_rows = []
    for col in np.transpose(fft_rows):
        fft_cols_rows.append(fft(col))
    fft_cols_rows = np.array(fft_cols_rows)

    ft_spectrum = np.abs(fft_cols_rows)
    shifted_spectrum = phase_shift(ft_spectrum)

    plt.axis('off')
    if show_plot:

        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
            plt.title('Custom, Slow FFT (logarithmic)')
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
            plt.title('Custom, Slow FFT (normal)')
        plt.show()

    if output:
        if logarithmic:
            plt.imshow(np.log(shifted_spectrum + 1), cmap='gray')
            plt.title('Custom, Slow FFT (logarithmic)')
            plt.savefig(output)
        else:
            plt.imshow(shifted_spectrum, cmap='gray')
            plt.title('Custom, Slow FFT (normal)')
            plt.savefig(output)


    return fft_cols_rows


# def visualize_spectrum(image_fft):
#     spectrum = np.log(np.abs(image_fft) + 1)
#     shifted_spectrum = phase_shift(spectrum)
#
#     plt.imshow(shifted_spectrum, cmap='gray')
#     plt.title("Fourier Spectrum")
#     plt.show()


def visualize_image(image_fft, output):
    # without logarithmic function there is only one dot in the middle
    image_magnitude = np.abs(image_fft)
    shifted_image = phase_shift(image_magnitude)

    plt.subplot(1, 2, 1)
    plt.axis("off")
    plt.imshow(shifted_image, cmap='gray')
    plt.title("Frequency Domain (normal)")
    # plt.show()

    spectrum = np.log(np.abs(image_fft) + 1)
    shifted_spectrum = phase_shift(spectrum)
    plt.subplot(1, 2, 2)
    plt.axis("off")
    plt.imshow(shifted_spectrum, cmap='gray')
    plt.title("Frequency Domain (logarithmic)")
    plt.show()
    if output:
        plt.imsave(output, np.abs(shifted_spectrum), cmap='gray')


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


def ifft2d(image_fft, output=None, show=False):
    # Transpose the image to ensure proper calculation of rows and columns
    # otherwise it rotates the image by 90 degree
    transposed_image_fft = np.transpose(image_fft)

    # Apply ifft along rows
    ifft_rows = []
    for row in transposed_image_fft:
        ifft_rows.append(ifft(row))
    ifft_rows = np.array(ifft_rows)

    # Transpose the result and apply ifft along columns
    ifft_cols_rows = []
    for col in np.transpose(ifft_rows):
        ifft_cols_rows.append(ifft(col))
    ifft_cols_rows = np.array(ifft_cols_rows)

    if output:
        plt.imsave(output, np.abs(ifft_cols_rows), cmap='gray')
    if show:
        plt.imshow(np.abs(ifft_cols_rows), cmap='gray')
        plt.title("Reconstructed Image")
        plt.show()

    return ifft_cols_rows

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
