import support_functions as sp
from PIL import Image

def uniform_histogram(image, min_brightness, max_brightness, output):
    width, height = image.size
    histogram = [0] * 256  # Create a histogram with 256 bins.

    for x in range(width):
        for y in range(height):
            pixel_value = image.getpixel((x, y))
            histogram[pixel_value] += 1

    total_pixels = 0

    for count in histogram:
        total_pixels += count

    # cumulative_histogram, sums of pixel counts for different intensity values
    cumulative_histogram = [0]

    for intensity in range(1, 256):  # Go from 1 to 255. Intensity.
        previous_cumulative = cumulative_histogram[-1]  # -1 refers to the last element in a list
        current_cumulative = previous_cumulative + histogram[intensity]  # we calcuate new brightness based on the histogram
        cumulative_histogram.append(current_cumulative)

    new_image = Image.new(image.mode, (width, height)) # new image for both gray scale and RGB scle

    for x in range(width):
        for y in range(height):
            old_brightness = image.getpixel((x, y))  # gets the current brightness level of the pixel
            new_brightness = cumulative_histogram[old_brightness] * (max_brightness - min_brightness) / total_pixels  # function for new brightness
            new_image.putpixel((x, y), int(new_brightness + min_brightness))  # Update the pixel value.

    new_image.show()
    sp.save_image(new_image, output)
