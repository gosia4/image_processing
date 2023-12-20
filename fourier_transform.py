import numpy as np

from matplotlib import pyplot as plt

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


def fft_shift(arr):
    rows, cols = arr.shape
    mid_row, mid_col = rows // 2, cols // 2

    shifted_arr = np.empty_like(arr, dtype=np.complex128)

    for i in range(mid_row):
        for j in range(mid_col):
            shifted_arr[i, j] = arr[i + mid_row, j + mid_col]
            shifted_arr[i + mid_row, j + mid_col] = arr[i, j]
            shifted_arr[i, j + mid_col] = arr[i + mid_row, j]
            shifted_arr[i + mid_row, j] = arr[i, j + mid_col]

    return shifted_arr


def plot_fourier_transform(image):
    fourier_transform = dft2d(image)
    shifted_transform = fft_shift(fourier_transform)
    magnitude_spectrum = np.log(np.abs(shifted_transform) + 1)

    plt.subplot(1, 1, 1)
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title('Amplituda Transformaty Fouriera')
    plt.colorbar()

    plt.show()
