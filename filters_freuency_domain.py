import matplotlib.pyplot as plt
import numpy as np
import fourier_transform as ft


#  remove high frequency components
#  used to smooth the image (blur)
#  remove noise
def low_pass_filter(image, D0, output): # D0 - non-negative integer
    image_fft = ft.fft2d(image)
    M, N = image_fft.shape
    H = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            D = np.sqrt((i - M//2) ** 2 + (j - N//2) ** 2)

            if D <= D0:
                H[i, j] = 0
            else:
                H[i, j] = 1
    # plt.subplot(1, 3, 1)
    # plt.imshow(H, cmap='gray')
    # plt.title('Filter')
    # plt.show()
    # we take into account average value of pixels in the frequency domain, as DC component
    H[M // 2, N // 2] = 1  # DC component

    image_fft_filtered = H * image_fft
    image_ifft_filtered = ft.ifft2d(image_fft_filtered, None, False)
    plt.imshow(np.real(image_ifft_filtered), cmap='gray')
    plt.title("Image after low-pass filter")
    plt.axis("off")
    plt.show()
    plt.imsave(output, np.real(image_ifft_filtered), cmap='gray')

    return image_ifft_filtered


def high_pass_filter(image, D0, output):
    image_fft = ft.fft2d(image)
    M, N = image_fft.shape
    H = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            D = np.sqrt((i - M // 2) ** 2 + (j - N // 2) ** 2)
            if D <= D0:
                H[i, j] = 1
            else:
                H[i, j] = 0

    H[M // 2, N // 2] = 0  # DC component not taken into account, as is it set to 0

    # applying the filter on the image
    image_fft_filtered = image_fft * H

    # Use inverse fourier transform to see the image in the spatial domain
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.real(image_filtered), cmap='gray')
    plt.axis("off")
    plt.title("Image after high-pass filter")
    plt.show()

    plt.imsave(output, np.real(image_filtered), cmap='gray')

    return image_filtered


def band_pass_filter(image, high_frequency, low_frequency, output):
    image_fft = ft.fft2d(image)
    M, N = image_fft.shape
    H = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            D = np.sqrt((i - M // 2) ** 2 + (j - N // 2) ** 2)
            if low_frequency <= D <= high_frequency:
                H[i, j] = 1
                # H[i, j] = 0
            else:
                # H[i, j] = 1
                H[i, j] = 0

    image_fft_filtered = H * image_fft
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title("Image after band-pass filter")
    plt.axis("off")
    plt.show()

    plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_filtered


# works good :-)
def band_cut_filter(image, treshold_1, treshold_2, output):
    image_fft = ft.fft2d(image)
    M, N = image_fft.shape
    H = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            D = np.sqrt((i - M // 2) ** 2 + (j - N // 2) ** 2)
            if treshold_1 <= D <= treshold_2:
                H[i, j] = 0
            else:
                H[i, j] = 1

    image_fft_filtered = H * image_fft
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title("Image after band-cut filter")
    plt.axis("off")
    plt.show()

    plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_filtered


# def high_pass_filter_with_edge_detection(image, high_frequency, low_frequency, mask, output=None):
#     # assuming that the mask and the image are the same size
#     image_fft = ft.fft2d(image)
#     M, N = image_fft.shape
#     # fill with ones
#     filtered_image = np.ones((M, N), dtype=np.float32)
#     mask_image = Image.open(mask)
#     mask_array = np.array(mask_image)
#     filtered_image *= mask_array
#
#     center_frequency = max(M, N) / 2
#     for i in range(M):
#         for j in range(N):
#             D = np.sqrt((i - M // 2) ** 2 + (j - N // 2) ** 2)
#             if D<= center_frequency - low_frequency /2 or D>=center_frequency + high_frequency /2:
#                 filtered_image[i, j] = 0
#
#
#     # Apply the filter to the image in the frequency domain
#     image_fft_filtered = filtered_image * image_fft
#
#     # Perform inverse FFT to get the spatial domain representation
#     # image_filtered = np.fft.ifft2(image_fft_filtered).real
#     image_filtered = ft.ifft2d(image_fft_filtered, None, False)
#     # Visualize the result
#     plt.imshow(np.abs(image_filtered), cmap='gray')
#     plt.title("Image after high-pass filter with edge detection")
#     plt.show()
#     plt.imsave(output, np.abs(filtered_image), cmap='gray')
