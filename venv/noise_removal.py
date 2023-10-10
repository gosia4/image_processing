import numpy as np
from PIL import Image
import statistics


def median_filter(im, value):
    temp = []
    im = Image.open("venv/images/lenac.bmp")
    arr = np.array(im.getdata())
    result_array = []
    result_array = np.zeros((len(arr), len(arr[0])))
    # print(len(arr[0]))
    # print(len(arr))
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            for z in range(value):
                if i + z - (value/2) < 0 or i + z - indexer > len(arr) - 1:
                    for c in range(value):
                        temp.apend(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(arr[0]) - 1:
                            temp.append(0)
                        else:
                            for k in range(value):
                                temp.append(arr[i + z - indexer][j + k - indexer])
        temp.sort()
        result_array[i][j] = temp[len(temp)//2]
        temp = []
    newIm = Image.fromarray(arr.astype(np.uint8))
    newIm.show()

    newIm.save("result.bmp")

im = Image.open("venv/images/lenac_impulse1.bmp")
data = np.array(im.getdata())
def median_filter2(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = np.zeros((len(data), len(data[0])))
    for i in range(len(data)):
        for j in range(len(data[0])):
            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    newIm = Image.fromarray(data_final.astype(np.uint8))
    newIm.show()
    #return data_final

def median_filter3(im, kernel_size):
    height, width = im.size
    half_kernel = kernel_size // 2
    #filtered_image = np.zeros((height, width), dtype=np.uint8)
    arr = np.array(im.getdata())
    filtered_image = np.zeros((len(arr), len(arr[0])))
    for i in range(height):
        for j in range(width):
            for z in range(kernel_size):
                #statistics.median(arr)
                window = im[max(0, i - half_kernel):min(height, i + half_kernel + 1),
                         max(0, j - half_kernel):min(width, j + half_kernel + 1)]
                filtered_image[i, j] = np.median(window)

    filtered_image.show()

def median_filter4(im, filter_size):
    data = np.array(im.getdata())
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = np.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    newIm = Image.fromarray(data_final.astype(np.uint8))
    newIm.show()

def remove_noise_median(image, kernel_size):
    width, height = image.size
    print(image.mode)
    filtered_image = Image.new("L", (width, height))

    for x in range(width):
        for y in range(height):

            sample_arr = []

            for i in range(-kernel_size // 2 + 1, kernel_size // 2 + 1):
                for j in range(-kernel_size // 2 + 1, kernel_size // 2 + 1):

                    target_x = x + i
                    target_y = y + j

                    if (target_x >= 0 and target_x < width - 1):
                        if (target_y >= 0 and target_y < height - 1):
                            sample_arr.append(image.getpixel((target_x, target_y)))

            sample_arr.sort()
            if (kernel_size % 2):
                median = sample_arr[len(sample_arr) // 2]

            else:
                median = int((sample_arr[len(sample_arr) // 2] + sample_arr[len(sample_arr) // 2 + 1]) / 2)

            filtered_image.putpixel((x, y), median)


    filtered_image.save("new_image.bmp")
    filtered_image.show()
