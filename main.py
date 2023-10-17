import sys

import error_functions
import geometric_operations
import basic_operations
import noise_removal
from PIL import Image
import numpy as np

# noise_removal.remove_noise_median(Image.open("lena_impulse3.bmp"), 3)

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
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        basic_operations.modify_brightness(Image.open(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--contrast":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        basic_operations.modify_contrast(Image.open(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--negative":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        basic_operations.apply_negative(Image.open(sys.argv[2]), sys.argv[3])
elif sys.argv[1] == "--hflip":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.horizontal_flip(Image.open(sys.argv[2]), sys.argv[3])
elif sys.argv[1] == "--vflip":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.vertical_flip(Image.open(sys.argv[2]), sys.argv[3])
elif sys.argv[1] == "--dflip":
    if len(sys.argv) != 2:
        print("Unexpected argument for --dflip.")
    else:
        geometric_operations.diagonal_flip(Image.open(sys.argv[2]), sys.argv[3])
elif sys.argv[1] == "--shrink":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.shrinking(Image.open(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--zoomin":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.shrink(Image.open(sys.argv[2]), sys.argv[3])
elif sys.argv[1] == "--enlarge":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.enlarge_image(Image.open(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--median":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        noise_removal.remove_noise_median(Image.open(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--gmean":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        noise_removal.geometric_mean(Image.open(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--mse":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        print(error_functions.mse(Image.open(sys.argv[2]), Image.open(sys.argv[3])))
elif sys.argv[1] == "--pmse":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        print(error_functions.pmse(Image.open(sys.argv[2]), Image.open(sys.argv[3])))
elif sys.argv[1] == "--snr":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        print(error_functions.snr(Image.open(sys.argv[2]), Image.open(sys.argv[3])))
elif sys.argv[1] == "--psnr":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        print(error_functions.mse(Image.open(sys.argv[2]), Image.open(sys.argv[3])))
elif sys.argv[1] == "--md":
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        print(error_functions.md(Image.open(sys.argv[2]), Image.open(sys.argv[3])))
elif sys.argv[1] == "--help":
    if len(sys.argv) != 2:
        print("Unexpected argument for --help.")
    else:
        show_help()
else:
    print("This command does not exist")
