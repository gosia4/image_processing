from PIL import Image
import basic_operations
import geometric_operations

# def main():
im = Image.open("venv/images/lenac.bmp")


def show_help():
    print("Basic operations:\n"
          "--brightness parameter, modifies brightness by a parameter"
          "\nas a parameter provide values from bigger than 0 to make the image lighter"
          "\nas a parameter provide values smaller than 0 to make the image dunkler"
          "\n\n--contrast parameter, modifies contrast by a parameter"
          "\nas a parameter provide values between 0 and 10 to change the contrast"
          "\n\n--negative, without parameter"
          "\n\n--hflip, without parameter, horizontal flip"
          "\n\n--vflip, without parameter, vertical flip"
          "\n\n--dflip, without parameter, diagonal flip"
          "\n\n--shrink parameter, shrink the image"
          "\nas a parameter provide a factor"
          "\n\n--enlarge parameter, enlarge the image"
          "\nas a parameter provide a factor")


print(
    "This is an image processing application. Write a command to begin or --help to see all the available commands.\n")
x = input()
new_x = x.split(' ')
if new_x[0] == "--brightness":
    basic_operations.modify_brightness2(im, int(new_x[1]))
if new_x[0] == "--contrast":
    basic_operations.modify_contrast3(im, int(new_x[1]))
if new_x[0] == "--negative":
    basic_operations.apply_negative(im)
if new_x[0] == "--hflip":
    geometric_operations.horizontal_flip(im)
if new_x[0] == "--vflip":
    geometric_operations.vertical_flip(im)
if new_x[0] == "--dflip":
    geometric_operations.diagonal_flip(im)
if new_x[0] == "--help":
    show_help()

# example
geometric_operations.enlarge(im, 2)
# show_help()


# # im = Image.open("lena.bmp")
#
# arr = np.array(im.getdata())
# print(im.getdata()[0])
# if arr.ndim == 1:  # grayscale
#     numColorChannels = 1
#     arr = arr.reshape(im.size[1], im.size[0])
# else:
#     numColorChannels = arr.shape[1]
#     arr = arr.reshape(im.size[1], im.size[0], numColorChannels)


# arr.reshape(2, 393216)
# print(im.size[1])
# print(im.size[0])
# print(arr)
# arr = arr - 30  # Example processing (decrease brightness)

# newIm = Image.fromarray(arr.astype(np.uint8))
# newIm.show()

# newIm.save("result.bmp")
# def save_image(image, output_path):
#     image.save(output_path)


# def modify_brightness(image, factor):
#     arr = np.array(image)
#     arr = arr * factor
#     arr = np.clip(arr, 0, 255).astype(np.uint8)
#     save_image(Image.fromarray(arr), "new_image.bmp")
# return Image.fromarray(arr)


# example
# new_image = modify_brightness(im, 1/30)
# save_image(arr, "new_image.bmp")


# from PIL import Image
# import numpy as np
#
# im = Image.open("venv/images/lenac.bmp")
# # im = Image.open("lena.bmp")
#
# arr = np.array(im.getdata())
# if arr.ndim == 1:  # grayscale
#     numColorChannels = 1
#     arr = arr.reshape(im.size[1], im.size[0])
# else:
#     numColorChannels = arr.shape[1]
#     arr = arr.reshape(im.size[1], im.size[0], numColorChannels)


# arr = arr / 2 # Example processing (decrease brightness)

# def brightness(img, strength=0):
#     return [[[
#         int((510 / (1 + (2.7183 ** (-strength * img[i][j][k] / 255)))) - 255)
#         for k in range(len(img[0][0]))
#     ] for j in range(len(img[0]))] for i in range(len(img))]
#
#
# brightness(arr, 0)
#
# newIm = Image.fromarray(arr.astype(np.uint8))
# newIm.show()
#
# newIm.save("result.bmp")
