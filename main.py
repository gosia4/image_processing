import sys

import error_functions
import geometric_operations
import basic_operations
import noise_removal
from PIL import Image
import numpy as np

# def main():
im = Image.open("venv/images/lenac.bmp")
# im1 = Image.open("venv/images/lenac_uniform1.bmp")
# noise_removal.geometric_mean(im1, 3)


# print(error_functions.psnr(im, im1))
# im1 = Image.open("new_image.bmp")
# print(error_functions.mse(im, noise_removal.remove_noise_median(im1, 3)))


def show_help():
    print("Basic operations:\n\n"
          "--brightness parameter: modifies brightness by a parameter"
          "\nas a parameter provide values 0 to 255 to make the image lighter"
          "\nas a parameter provide values -255 to 0 to make the image darker"
          "\n\n--contrast parameter: modifies contrast by a parameter"
          "\nas a parameter provide values between 0 and 10 to change the contrast"
          "\n\n--negative: changes the negative of the image; without parameter"
          "\n\n--hflip: horizontal flip of the image; without parameter"
          "\n\n--vflip: vertical flip of the image; without parameter"
          "\n\n--dflip:diagonal flip of the image; without parameter"
          "\n\n--shrink: shrink the image by a value"
          "\nas a parameter provide a factor"
          "\n\n--zoomin: zoom in the image; without parameter"
          "\n\n--enlarge parameter, enlarge the image by a value"
          "\nas a parameter provide a factor"
          "\n\n--median: reduces the noise of the image using median filter"
          "\nas a parameter provide the kernel size >=3"
          "\n\n--gmean: reduces the noise of the image using geometric mean filter"
          "\nas a parameter provide the kernel size"
          "\n\n--mse: Mean square error"
          "\n\n--pmse: Peak mean square error"
          "\n\n--snr: Signal to noise ratio"
          "\n\n--psnr: Peak signal to noise ratio"
          "\n\n--md: Maximum difference")


if len(sys.argv) < 2:
    print("Please provide a command.")
elif sys.argv[1] == "--brightness":
    if len(sys.argv) < 3:
        print("Please provide a brightness value.")
    else:
        basic_operations.modify_brightness(im, int(sys.argv[2]))
elif sys.argv[1] == "--contrast":
    if len(sys.argv) < 3:
        print("Please provide a contrast value.")
    else:
        basic_operations.modify_contrast(im, int(sys.argv[2]))
elif sys.argv[1] == "--negative":
    if len(sys.argv) != 2:
        print("Unexpected argument for --negative.")
    else:
        basic_operations.apply_negative(im)
elif sys.argv[1] == "--hflip":
    if len(sys.argv) != 2:
        print("Unexpected argument for --hflip.")
    else:
        geometric_operations.horizontal_flip(im)
elif sys.argv[1] == "--vflip":
    if len(sys.argv) != 2:
        print("Unexpected argument for --vflip.")
    else:
        geometric_operations.vertical_flip(im)
elif sys.argv[1] == "--dflip":
    if len(sys.argv) != 2:
        print("Unexpected argument for --dflip.")
    else:
        geometric_operations.diagonal_flip(im)
elif sys.argv[1] == "--shrink":
    if len(sys.argv) < 3:
        print("Please provide a shrink factor.")
    else:
        geometric_operations.shrinking(im, float(sys.argv[2]))
elif sys.argv[1] == "--zoomin":
    if len(sys.argv) != 2:
        print("Unexpected argument for --zoomin.")
    else:
        geometric_operations.shrink(im)
elif sys.argv[1] == "--enlarge":
    if len(sys.argv) < 3:
        print("Please provide an enlargement factor.")
    else:
        geometric_operations.enlarge_image(im, float(sys.argv[2]))
elif sys.argv[1] == "--median":
    if len(sys.argv) < 3:
        print("Please provide a kernel size for median filtering.")
    else:
        noise_removal.remove_noise_median(im, int(sys.argv[2]))
elif sys.argv[1] == "--gmean":
    if len(sys.argv) < 3:
        print("Please provide a kernel size for geometric mean filtering.")
    else:
        noise_removal.geometric_mean(im, int(sys.argv[2]))
elif sys.argv[1] == "--mse":
    if len(sys.argv) < 4:
        print("Please provide a ")
    else:
        print(error_functions.mse(Image.open(sys.argv[2]), Image.open(sys.argv[3])))
elif sys.argv[1] == "--pmse":
    if len(sys.argv) != 2:
        print("Unexpected argument for --pmse.")
    else:
        print(error_functions.pmse(int(sys.argv[2]), int(sys.argv[3])))
elif sys.argv[1] == "--snr":
    if len(sys.argv) != 2:
        print("Unexpected argument for --snr.")
    else:
        print(error_functions.snr(int(sys.argv[2]), int(sys.argv[3])))
elif sys.argv[1] == "--psnr":
    if len(sys.argv) != 2:
        print("Unexpected argument for --psnr.")
    else:
        print(error_functions.mse(int(sys.argv[2]), int(sys.argv[3])))
elif sys.argv[1] == "--md":
    if len(sys.argv) != 2:
        print("Unexpected argument for --md.")
    else:
        print(error_functions.mse(im, im1))
elif sys.argv[1] == "--help":
    if len(sys.argv) != 2:
        print("Unexpected argument for --help.")
    else:
        show_help()
else:
    print("This command does not exist")

# if sys.argv[1] == "--brightness":
#     basic_operations.modify_brightness(im, int(sys.argv[2]))
# if sys.argv[1] == "--contrast":
#     basic_operations.modify_contrast(im, int(sys.argv[2]))
# elif sys.argv[1] == "--negative":
#     basic_operations.apply_negative(im)
# elif sys.argv[1] == "--hflip":
#     geometric_operations.horizontal_flip(im)
# elif sys.argv[1] == "--vflip":
#     geometric_operations.vertical_flip(im)
# elif sys.argv[1] == "--dflip":
#     geometric_operations.diagonal_flip(im)
# elif sys.argv[1] == "--shrink":
#     geometric_operations.shrinking(im, sys.argv[2])
# elif sys.argv[1] == "--enlarge":
#     geometric_operations.enlarge_image(im, sys.argv[2])
# elif sys.argv[1] == "--median":
#     noise_removal.remove_noise_median(im, sys.argv[2])
# elif sys.argv[1] == "--gmean":
#     noise_removal.geometric_mean(im, sys.argv[2])
# elif sys.argv[1] == "--mse":
#     print(error_functions.mse(im, im1))  # czy użytkownik ma podać nazwy pliku z obrazkiem?
# elif sys.argv[1] == "--pmse":
#     print(error_functions.pmse(im, im1))  # czy użytkownik ma podać nazwy pliku z obrazkiem?
# # elif sys.argv[1] == "--snr":
# #     error_functions.snr(sys.argv[1], sys.argv[2])  # czy użytkownik ma podać nazwy pliku z obrazkiem?
# elif sys.argv[1] == "--help":
#     show_help()
# else:
#     print("This command does not exist")
