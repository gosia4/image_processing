import numpy as np
from PIL import Image
import math

def save_image(image, output_path):
    image.save(output_path)


def modify_brightness(image, factor):
    arr = np.array(image)
    if (factor == 0): print("O is not allowed")
    else: arr = arr / factor
    # arr = arr * factor
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    save_image(Image.fromarray(arr), "new_image.bmp")

def modify_brightness2(image, factor):
    if factor < -255: factor = -255
    if factor > 255: factor = 255
    width, height = image.size
    result_image = Image.new('RGB', (width, height))
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            new_r = r + factor
            new_g = g + factor
            new_b = b + factor

            result_image.putpixel((x, y), (int(new_r), int(new_g), int(new_b)))
    result_image.save("new_image.bmp")


# def modify_contrast(image, factor):
#     arr = np.array(image)
#     # Wyśrodkowujemy piksele, zmieniamy kontrast i potem wracamy do pierwotnego ułożenia
#     new_image_array = (arr - 128) * factor + 128
#
#     # Trzeba się upewnić, żeby piksele były od 0 to 255, albo może nie?
#     new_image_array = np.clip(new_image_array, 0, 255).astype(np.uint8)
#
#     save_image(Image.fromarray(new_image_array), "new_image.bmp")


# def modify_contrast2(image, factor):
#     width, height = image.size
#     result_image = Image.new('RGB',(width, height))
#     for y in range(height):
#         for x in range(width):
#             r, g, b = image.getpixel((x, y))
#
#             new_r = r + ((r - 128) * factor)
#             new_g = g + ((g - 128) * factor)
#             new_b = b + ((b - 128) * factor)
#
#             result_image.putpixel((x, y), (int(new_r), int(new_g), int(new_b)))
#     result_image.save("new_image.bmp")
#     result_image.show()

def modify_contrast3(image, factor):
    color_channels = 0
    if factor > 10:
        factor = 10
    if factor < -10:
        factor = -10
    width, height = image.size
    lut = []

    # look up table creation
    for i in range(256):
        new = 128 + ((i - 128) * (math.e ** (factor)))
        lut.append(new)

    if (image.mode == "RGB"):
        result_image = Image.new('RGB', (width, height))
        color_channels = 3
    elif (image.mode == "L"):
        result_image = Image.new('RGB', (width, height))
        color_channels = 1

    if (color_channels == 0):
        print("this program does not support this color model.")
        return

    for y in range(height):
        for x in range(width):
            old_value = image.getpixel((x, y))[0]
            new_value = lut[old_value]

            result_image.putpixel((x, y), new_value)
    result_image.save("new_image.bmp")
    result_image.show()

def apply_negative(image):
    width, height = image.size
    negative_image = Image.new('RGB',(width, height))
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            # dla każdego RGB obiczmy nagtyw
            negative_r = 255 - r
            negative_g = 255 - g
            negative_b = 255 - b

            negative_image.putpixel((x, y), (negative_r, negative_g, negative_b))
    negative_image.show()
    negative_image.save("new_image.bmp")