import numpy as np
from PIL import Image
import support_functions as sp


def remove_noise_median(image, kernel_size):
    width, height = image.size

    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("this program does not support this color model.")
        return

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
            median_pixel = []
            for c in range(color_channels):
                channel_arr = []
                for h in range(len(sample_arr)):
                    channel_arr.append(sp.int_or_tuple_to_array(sample_arr[h])[c])

                channel_arr.sort()

                middle_number = len(channel_arr) // 2
                if kernel_size % 2:
                    median_pixel.append(channel_arr[middle_number])

                else:
                    median_pixel.append((channel_arr[middle_number] + channel_arr[middle_number + 1]) // 2)

            result_image.putpixel((x, y), tuple(median_pixel))

    result_image.save("new_image.bmp")
    result_image.show()


