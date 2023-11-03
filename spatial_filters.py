import support_functions as sp
from PIL import Image
import numpy as np


def uniform_histogram(image, min_brightness, max_brightness, output):
    if sp.analyse_color_channels(image)[1] == 1:
        width, height = image.size

        histogram = sp.calculate_histogram(image)

        total_pixels = 0

        for count in histogram:
            total_pixels += count

        # cumulative_histogram, sums of pixel counts for different intensity values
        cumulative_histogram = [0]

        for intensity in range(1, 256):  # Go from 1 to 255. Intensity.
            previous_cumulative = cumulative_histogram[-1]  # -1 refers to the last element in a list
            current_cumulative = previous_cumulative + histogram[
                intensity]  # we calcuate new brightness based on the histogram
            cumulative_histogram.append(current_cumulative)

        new_image = Image.new(image.mode, (width, height))  # new image for both gray scale and RGB scle

        for x in range(width):
            for y in range(height):
                old_brightness = image.getpixel((x, y))  # gets the current brightness level of the pixel
                new_brightness = cumulative_histogram[old_brightness] * (
                            max_brightness - min_brightness) / total_pixels  # function for new brightness
                new_image.putpixel((x, y), int(new_brightness + min_brightness))  # Update the pixel value.

        new_image.show()
        sp.save_image(new_image, output)
    else:
        uniform_histogram_color(image, min_brightness, max_brightness, output)


def uniform_histogram_color(image, min_brightness, max_brightness, output):
    width, height = image.size

    histogram_r = [0] * 256
    histogram_g = [0] * 256
    histogram_b = [0] * 256

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            histogram_r[r] += 1
            histogram_g[g] += 1
            histogram_b[b] += 1

    total_pixels = width * height

    cumulative_histogram_r = [0]
    cumulative_histogram_g = [0]
    cumulative_histogram_b = [0]

    cumulative_r = 0
    cumulative_g = 0
    cumulative_b = 0

    for i in range(256):
        cumulative_r += histogram_r[i]
        cumulative_histogram_r.append(cumulative_r)

        cumulative_g += histogram_g[i]
        cumulative_histogram_g.append(cumulative_g)

        cumulative_b += histogram_b[i]
        cumulative_histogram_b.append(cumulative_b)

    new_image = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))

            new_r = int(cumulative_histogram_r[r] * (max_brightness - min_brightness) / total_pixels + min_brightness)
            new_g = int(cumulative_histogram_g[g] * (max_brightness - min_brightness) / total_pixels + min_brightness)
            new_b = int(cumulative_histogram_b[b] * (max_brightness - min_brightness) / total_pixels + min_brightness)

            new_image.putpixel((x, y), (new_r, new_g, new_b))

    new_image.show()
    new_image.save(output)


def edge_sharpening(image, kernel_size, output):
    kernel_size = int(kernel_size)
    if kernel_size < 3:
        print("Kernel size must be at least 3")
        return

    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)

    if color_channels == 0:
        print("This program does not support this color model.")
        return

    # Define a Laplacian kernel for edge sharpening
    laplacian_kernel = [[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]]

    for x in range(width):
        for y in range(height):
            new_pixel = [0] * color_channels

            for i in range(-kernel_size // 2 + 1, kernel_size // 2 + 1):
                for j in range(-kernel_size // 2 + 1, kernel_size // 2 + 1):

                    target_x = x + i
                    target_y = y + j

                    if 0 <= target_x < width - 1:
                        if 0 <= target_y < height - 1:
                            pixel = image.getpixel((target_x, target_y))
                            if color_channels == 1:
                                new_pixel[0] += pixel * laplacian_kernel[i + kernel_size // 2][j + kernel_size // 2]
                            else:
                                for c in range(color_channels):
                                    new_pixel[c] += pixel[c] * laplacian_kernel[i + kernel_size // 2][j + kernel_size // 2]

            # new_pixel = [int(val) for val in new_pixel]
            for i in range(len(new_pixel)):
                new_pixel[i] = int(new_pixel[i])

            result_image.putpixel((x, y), tuple(new_pixel))

    sp.save_image(result_image, output)
    result_image.show()
