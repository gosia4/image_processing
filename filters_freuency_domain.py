import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from numpy.fft import ifftshift
from scipy.fft import ifft2, ifftshift, fftshift

import fourier_transform as ft


# so far: filter - white circle in the middle
#  remove high frequency components
#  used to smooth the image (blur)
#  remove noise
# TODO: apply on the image and display the filtered image, nad save the image
def low_pass_filter(image, D0): # D0 - non-negative integer
    image_fft = np.fft.fft2(image)
    M, N = image_fft.shape
    H = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            D = np.sqrt((i - M//2) ** 2 + (j - N//2) ** 2)
            if D > D0:
                H[i, j] = 0
            else:
                H[i,j] = 1
    # plt.subplot(1, 3, 1)
    plt.imshow(H, cmap='gray')
    plt.title('Filter')
    plt.show()

    return H





# something is wrong
def low_pass_filter2(image, D0):
    M, N = image.size
    H = np.zeros((M, N), dtype=np.float32)
    # D0 = 50
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-M/2)**2 + (v-N/2) ** 2)
            if D <= D0:
                H[u, v] = 1
            else:
                H[u, v] = 0
    # plt.imshow(H, cmap='gray')
    # plt.axis('off')
    # plt.show()

    # Przesunięcie i transpozycja filtru
    H_shifted = ft.phase_shift(np.transpose(H))
    # H_shifted = fftshift(H)

    # Obliczenia FFT obrazu
    img_fft = ft.fft2d(image)

    # Przesunięcie i transpozycja FFT obrazu
    image_fft_shifted = ft.phase_shift(np.transpose(img_fft))
    # image_fft_shifted = fftshift(img_fft)
    # Przemnożenie FFT obrazu przez filtr
    image_with_filter = H_shifted * image_fft_shifted

    # Przesunięcie i transpozycja odwrotnego FFT
    image_inverse_fft_shifted = ft.phase_shift(np.fft.ifftshift(image_with_filter))

    # Obliczenia odwrotnej FFT
    # image_filtered = np.fft.ifft2(image_inverse_fft_shifted).real
    image_filtered = ft.ifft2d(image_inverse_fft_shifted)

    # diplay filter
    plt.subplot(1, 3, 1)
    plt.imshow(H, cmap='gray')
    plt.title('Filter')

    # Wyświetl obraz po filtracji
    plt.subplot(1, 3, 2)
    plt.imshow(np.log(1 + np.abs(image_fft_shifted)), cmap='gray')
    plt.title('Shifted Spectrum')

    plt.subplot(1, 3, 3)
    plt.imshow(np.abs(image_filtered), cmap='gray')
    plt.title('Filtered Image')

    plt.show()
    # obraz obrócony o 90 stopni
    # Image.fromarray(image_filtered).show()

    # Image.fromarray(image_filtered.transpose()).show()
    # Image.fromarray(np.abs(image_filtered).astype(np.uint8)).show()

    return image_filtered

