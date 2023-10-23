import sys
from PIL import Image
import error_functions
import geometric_operations
import basic_operations
import noise_removal

noise_removal.remove_noise_median(Image.open("lena_impulse1.bmp"), 3 ,"new_image.bmp")

def show_help():
    print("---------------Basic operations:-----------------\n"
          "\n"
          "--brightness: modifies brightness of the image by value\n"
          "\tuse case: --brightness [image_path] [value] [output_path]\n"
          "\t\t[value] is added to every pixel of the image,\n"
          "\t\tto make image brighter provide positive value,\n"
          "\t\tfor darker provide negative value\n"
          "\n"
          "--contrast: modifies contrast of the image by value\n"
          "\tuse case: --contrast [image_path] [value] [output_path]\n"
          "\t\t[value] is used for a contrast modification formula,\n"
          "\t\tto increase the contrast provide number from 1 to 10\n"
          "\t\tto decrease the contrast provide number from -10 to -1\n"
          "\n"
          "--negative: creates the negative of the image\n"
          "\tuse case: --negative [image_path] [output_path]\n"
          "\n"
          "-------------Geometric operations:----------------\n"
          "\n"
          "--hflip: flips the image horizontally\n"
          "\tuse case: --hflip [image_path] [output_path]\n"
          "\n"
          "--vflip: flips the image vertically\n"
          "\tuse case: --vflip [image_path] [output_path]\n"
          "\n"
          "--dflip: flips the image diagonally\n"
          "\tuse case: --vflip [image_path] [output_path]\n"
          "\n"
          "--shrink: shrinks the image by value\n"
          "\tuse case: --shrink [image_path] [value] [output_path]\n"
          "\t\t[value] describes the proportions between original size and output image size.\n"
          "\t\tThe output image will be [value] times smaller than the original image.\n"
          "\n"
          "--enlarge: enlarges the image by value\n"
          "\tuse case: --enlarge [image_path] [value] [output_path]\n"
          "\t\t[value] describes the proportions between output image size and original size.\n"
          "\t\tThe output image will be [value] times larger than the original image.\n"
          "\n"
          "------------------Noise Filters:------------------\n"
          "\n" 
          "--median: reduces the noise of the image using median filter\n"
          "\tuse case: --median [image_path] [kernel_size] [output_path]\n"
          "\t\t[kernel_size] describes the dimensions of samples that filter will be using (minimum 3).\n"
          "\t\tFor best performance provide the [kernel size] == 3\n"
          "\n"
          "--gmean: reduces the noise of the image using geometric mean filter\n"
          "\tuse case: --gmean [image_path] [kernel_size] [output_path]\n"
          "\t\t[kernel_size] describes the dimensions of samples that filter will be using (minimum 3).\n"
          "\t\tFor best performance provide the [kernel size] == 3\n"
          "\n"
          "---------------Error Calculation:-----------------\n"
          "\n"
          "--mse: returns Mean square error value for pair of images\n"
          "\tuse case: --mse [first_image_path] [second_image_path]\n"
          "\t\tMse will be calculated regarding individual pixels of those 2 images.\n"
          "\t\tFirst image is treated as original image and second one as it's modification.\n"
          "\n"
          "--pmse: returns Peak mean square error value for pair of images\n"
          "\tuse case: --pmse [first_image_path] [second_image_path]\n"
          "\t\tPmse will be calculated regarding individual pixels of those 2 images.\n"
          "\t\tFirst image is treated as original image and second one as it's modification.\n"
          "\n"
          "--snr: returns Signal to noise ratio value for pair of images\n"
          "\tuse case: --snr [first_image_path] [second_image_path]\n"
          "\t\tSnr will be calculated regarding individual pixels of those 2 images.\n"
          "\t\tFirst image is treated as original image and second one as it's modification.\n"
          "\n"
          "--psnr: returns Peak signal to noise ratio value for pair of images\n"
          "\tuse case: --psnr [first_image_path] [second_image_path]\n"
          "\t\tPsnr will be calculated regarding individual pixels of those 2 images.\n"
          "\t\tFirst image is treated as original image and second one as it's modification.\n"
          "\n"
          "--md: returns Maximum differencevalue for pair of images\n"
          "\tuse case: --md [first_image_path] [second_image_path]\n"
          "\t\tMd will be calculated regarding individual pixels of those 2 images.\n"
          "\t\tFirst image is treated as original image and second one as it's modification.\n"
          )

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
    if len(sys.argv) < 4:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.diagonal_flip(Image.open(sys.argv[2]), sys.argv[3])
elif sys.argv[1] == "--shrink":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.scale(Image.open(sys.argv[2]), 1.0/float(sys.argv[3]), sys.argv[4])
elif sys.argv[1] == "--enlarge":
    if len(sys.argv) < 5:
        print("Please provide a correct number of parameters.")
    else:
        geometric_operations.scale(Image.open(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
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
