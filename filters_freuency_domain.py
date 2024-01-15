import matplotlib.pyplot as plt
import numpy as np
import fourier_transform as ft

def low_pass_filter(image, D0, spectrum=False, spectrumf=False, output=None):  # D0 - non-negative integer

    image_fft = ft.fft2d(image)
    M, N = image_fft.shape
    H = np.ones((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            D = np.sqrt((i - M//2) ** 2 + (j - N//2) ** 2)

            if D <= D0:
                H[i, j] = 0
            # else:
            #     H[i, j] = 1
    if spectrumf is True:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()

    image_fft_filtered = H * image_fft
    if spectrum is True:
        visualize_spectrum(image_fft_filtered)
    image_ifft_filtered = ft.ifft2d(image_fft_filtered, None, False)
    # plt.imshow(np.real(image_ifft_filtered), cmap='gray')
    plt.imshow(np.abs(image_ifft_filtered), cmap='gray')
    plt.title("Image after low-pass filter")
    plt.axis("off")
    plt.show()

    if output:
        plt.imsave(output, np.abs(image_ifft_filtered), cmap='gray')

    return image_ifft_filtered


def high_pass_filter(image, D0, spectrum=False, spectrumf=False, output=None):
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
    if spectrumf is True:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()

    image_fft_filtered = image_fft * H
    if spectrum is True:
        visualize_spectrum(image_fft_filtered)

    # Use inverse fourier transform to see the image in the spatial domain
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    # plt.imshow(np.real(image_filtered), cmap='gray')
    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.axis("off")
    plt.title("Image after high-pass filter")
    plt.show()

    if output:
        plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_fft_filtered


def visualize_spectrum(image_fft):
    spectrum = np.log(np.abs(image_fft) + 1)
    shifted_spectrum = ft.phase_shift(spectrum)

    plt.imshow(shifted_spectrum, cmap='gray')
    plt.title("Fourier Spectrum")
    plt.show()


def band_pass_filter(image, high_frequency, low_frequency, spectrum=False, spectrumf=False, output=None):
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
    if spectrumf is True:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()
    image_fft_filtered = H * image_fft
    if spectrum is True:
        visualize_spectrum(image_fft_filtered)
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title("Image after band-pass filter")
    plt.axis("off")
    plt.show()

    if output:
        plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_filtered


def band_cut_filter(image, treshold_1, treshold_2, spectrum=False, spectrumf=False, output=None):
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
    if spectrumf is True:
        plt.imshow(H, cmap='gray')
        plt.axis("off")
        plt.title("Filter")
        plt.show()

    image_fft_filtered = H * image_fft
    if spectrum is True:
        visualize_spectrum(image_fft_filtered)
    image_filtered = ft.ifft2d(image_fft_filtered, None, False)

    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title("Image after band-cut filter")
    plt.axis("off")
    plt.show()

    if output:
        plt.imsave(output, np.abs(image_filtered), cmap='gray')

    return image_filtered


def phase_shift_filter(image, l, k, show_image=False, output=None):

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
    if show_image is True:
        plt.imshow(phase_shifted_image, cmap='gray')
        plt.title('Phase Shifted Image')
        plt.show()

    if output:
        plt.imsave(output, np.abs(phase_shifted_image), cmap='gray')

    return phase_shifted_image


def high_pass_with_edge_detection(image, mask, diameter, show_plot=False, output=None):
    image = image.convert('L')
    mask = mask.convert('L')

    # hp_image = high_pass_filter(image, diameter)
    frequency_image = ft.fft2d(image)

    output_frequency = image * mask
    image_highpass = ft.ifft2d(output_frequency)

    if show_plot:
        plt.figure(figsize=(10, 5))

        plt.subplot(121), plt.imshow(image, cmap='gray')
        plt.title('Original Image'), plt.axis('off')

        plt.subplot(122), plt.imshow(np.abs(image_highpass), cmap='gray')
        plt.title('High-pass Filtered Image (Edge Detection)'), plt.axis('off')

        plt.show()
    if output:
        plt.imsave(output, np.abs(image_highpass), cmap='gray')
