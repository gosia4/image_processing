import sys
import geometric_operations
import basic_operations
import noise_removal
from PIL import Image
import numpy as np

# def main():
im = Image.open("venv/images/lena_impulse1.bmp")
data = np.array(im.getdata())


# noise_removal.median_filter4(im, 10)
# noise_removal.geometric_mean(im, 3)
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


# geometric_operations.shrink(im)
# noise_removal.remove_noise_median(im, 3)
# geometric_operations.shrink(im)


if sys.argv[1] == "--brightness":
    basic_operations.modify_brightness(im, int(sys.argv[1]))
elif sys.argv[1] == "--contrast":
    basic_operations.modify_contrast(im, int(sys.argv[1]))
elif sys.argv[1] == "--negative":
    basic_operations.apply_negative(im)
elif sys.argv[1] == "--hflip":
    geometric_operations.horizontal_flip(im)
elif sys.argv[1] == "--vflip":
    geometric_operations.vertical_flip(im)
elif sys.argv[1] == "--dflip":
    geometric_operations.diagonal_flip(im)
elif sys.argv[1] == "--shrink":
    geometric_operations.shrinking(im, sys.argv[1])
elif sys.argv[1] == "--enlarge":
    geometric_operations.enlarge(im, sys.argv[1])
elif sys.argv[1] == "--mean":
    noise_removal.median_filter(im, 20)
elif sys.argv[1] == "--help":
    show_help()
else:
    print("This command does not exist")

# example
# geometric_operations.vertical_flip(im)
# show_help()
