from PIL import Image
import support_functions as sp


def horizontal_flip(image, output):
    width, height = image.size
    result_image = sp.analyse_color_channels(image)[0]

    for y in range(height):
        for x in range(width // 2):  # divide by 2 to avoid transforming the same elements multiple times
            left_pixel = image.getpixel((x, y))
            right_pixel = image.getpixel((width - x - 1, y))
            result_image.putpixel((x, y), right_pixel)
            result_image.putpixel((width - x - 1, y), left_pixel)
    sp.save_image(result_image, output)
    result_image.show()


def vertical_flip(image, output):
    width, height = image.size
    result_image = sp.analyse_color_channels(image)[0]
    for y in range(height // 2):
        for x in range(width):
            top_pixel = image.getpixel((x, y))
            bottom_pixel = image.getpixel((x, height - y - 1))
            result_image.putpixel((x, y), bottom_pixel)
            result_image.putpixel((x, height - y - 1), top_pixel)
    sp.save_image(result_image, output)
    result_image.show()


def diagonal_flip(image, output):
    width, height = image.size
    result_image = sp.analyse_color_channels(image)[0]
    for x in range(width):
        for y in range(height):
            result_image.putpixel((width - x - 1, height - y - 1), image.getpixel((x, y)))
    sp.save_image(result_image, output)
    result_image.show()


def scale(image, val, output):
    if val == 0:
        print("Error")
    if val < 0:
        print("Value must be more than 0")
    else:
        width, height = image.size
        new_width = int(width * val)
        new_height = int(height * val)
        if val > new_width or val > new_height:
            print("Error, value must be smaller than new width and new height of the image")
        else:

            if image.mode == "RGB":
                result_image = Image.new('RGB', (new_width, new_height))
                for y in range(new_height):
                    for x in range(new_width):
                        result_image.putpixel((x, y), tuple(image.getpixel((int(x / val), int(y / val)))))
            elif image.mode == "L":
                result_image = Image.new('L', (new_width, new_height))
                for y in range(new_height):
                    for x in range(new_width):
                        source_pixel = image.getpixel((int(x / val), int(y / val)))
                        result_image.putpixel((x, y), source_pixel)
            else:
                print("this program does not support this color model.")
                return [0, 0]
            sp.save_image(result_image, output)
            result_image.show()
            return result_image
