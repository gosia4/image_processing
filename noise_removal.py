import numpy as np
from PIL import Image

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
            if kernel_size % 2:
                median = sample_arr[len(sample_arr) // 2]

            else:
                median = int((sample_arr[len(sample_arr) // 2] + sample_arr[len(sample_arr) // 2 + 1]) / 2)

            filtered_image.putpixel((x, y), median)

    filtered_image.save("new_image.bmp")
    filtered_image.show()
