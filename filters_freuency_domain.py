import matplotlib.pyplot as plt
import numpy as np
import fourier_transform as ft
from scipy import ndimage


#  remove high frequency components
#  used to smooth the image (blur)
#  remove noise
def low_pass_filter(image, D0, output, spectrum=False, spectrumf=False):  # D0 - non-negative integer
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
    if spectrumf:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()

    image_fft_filtered = H * image_fft
    if spectrum:
        visualize_spectrum(image_fft_filtered)
    image_ifft_filtered = ft.ifft2d(image_fft_filtered, None, False)
    # plt.imshow(np.real(image_ifft_filtered), cmap='gray')
    plt.imshow(np.abs(image_ifft_filtered), cmap='gray')
    plt.title("Image after low-pass filter")
    plt.axis("off")
    plt.show()

    plt.imsave(output, np.abs(image_ifft_filtered), cmap='gray')

    return image_ifft_filtered

def low_pass_filter_2(image, cutoff):
    image_array = ft.fft2d(image)
    image_array = np.array(image_array)


def high_pass_filter(image, D0, output, spectrum=False, spectrumf=False):
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
    if spectrumf:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()

    image_fft_filtered = image_fft * H
    if spectrum:
        visualize_spectrum(image_fft_filtered)

    # Use inverse fourier transform to see the image in the spatial domain
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    # plt.imshow(np.real(image_filtered), cmap='gray')
    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.axis("off")
    plt.title("Image after high-pass filter")
    plt.show()

    plt.imsave(output, np.real(image_filtered), cmap='gray')

    return image_filtered


def visualize_spectrum(image_fft):
    spectrum = np.log(np.abs(image_fft) + 1)
    shifted_spectrum = ft.phase_shift(spectrum)

    plt.imshow(shifted_spectrum, cmap='gray')
    plt.title("Fourier Spectrum")
    plt.show()


def band_pass_filter(image, high_frequency, low_frequency, output, spectrum=False, spectrumf=False):
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
    # H[M // 2, N // 2] = 1
    if spectrumf:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()
    image_fft_filtered = H * image_fft
    if spectrum:
        visualize_spectrum(image_fft_filtered)
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title("Image after band-pass filter")
    plt.axis("off")
    plt.show()

    plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_filtered


def band_cut_filter(image, treshold_1, treshold_2, output, spectrum=False, spectrumf=False):
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
    if spectrumf:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()

    image_fft_filtered = H * image_fft
    if spectrum:
        visualize_spectrum(image_fft_filtered)
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title("Image after band-cut filter")
    plt.axis("off")
    plt.show()

    plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_filtered


def phase_shift_filter(image, l, k, output=None, show_image=False):

    M, N = image.size

    n = np.arange(M) - M // 2
    m = np.arange(N) - N // 2

    n, m = np.meshgrid(n, m)

    # Calculate shift according to formula from task F6
    phase_shift_x = -2 * np.pi * n * l / N
    phase_shift_y = -2 * np.pi * m * k / M
    phase_shift = np.exp(1j * (phase_shift_x + phase_shift_y + (k+l) * np.pi))

    fft = ft.fft2d(image)
    phase_shifted_fft = fft * phase_shift

    phase_shifted_image = np.abs(ft.ifft2d(phase_shifted_fft))

    plt.axis('off')
    if show_image:
        plt.imshow(phase_shifted_image, cmap='gray')
        plt.title('Phase Shifted Image')
        plt.show()
    if output:
        plt.savefig(output)

    return phase_shifted_image

def high_pass_with_edge_detection(image, radius):
    rows, cols = image.size
    center_x, center_y = rows // 2, cols // 2

    f_transform = ft.phase_shift(ft.fft2d(image))

    # Create a mask with a high-pass filter
    mask = np.ones((rows, cols), np.uint8)
    center = [center_x, center_y]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius * radius
    mask[mask_area] = 0

    f_transform_highpass = f_transform * mask

    # Inverse Fourier Transform using the custom implementation
    image_highpass = ft.ifft2d(f_transform_highpass)

    # Display the original and high-pass filtered images using Matplotlib
    plt.figure(figsize=(10, 5))

    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Original Image'), plt.axis('off')

    plt.subplot(122), plt.imshow(np.abs(image_highpass), cmap='gray')
    plt.title('High-pass Filtered Image (Edge Detection)'), plt.axis('off')

    plt.show()



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
