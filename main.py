import sys
from PIL import Image

import error_functions
import geometric_operations
import basic_operations
import noise_removal
import spatial_filters
import characteristics

# geometric_operations.horizontal_flip(Image.open("lena.bmp"), "new_image.bmp")
# spatial_filters.uniform_histogram(Image.open("lenac.bmp"), 0, 1110, "new_image.bmp")
# characteristics.mean(Image.open("lena.bmp"))
# characteristics.mean(Image.open("lenac.bmp"))
# characteristics.variance(Image.open("lena.bmp"))
# print(characteristics.information_source_entropy(Image.open("lenac.bmp")))
# spatial_filters.edge_sharpening(Image.open("lena.bmp"), 3, "new_image.bmp")
import support_functions as sp
spatial_filters.uniform_fpd(Image.open("lena.bmp"), 20, 180, "new_image.bmp")

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
          "\n"
          "---------------Filtration in spatial domain  :-----------------\n"
          "\n"
          "--uhistogram: Uniform final probability density function, improves image quality\n"
          "\tuse case: --uhistogram [image_path] [min_brightness] [max_brightness] [output_path]\n"
          "\t\tUniform histogram describes the distribution of pixel intensities\n"
          "\t\tAfter transformation all pixel values within the specified range (min_brightness and max_brightness)\n"
          "\t\tare equally likely, resulting in a uniform distribution.\n"
          "\n"
          "--mean: calculates the mean value of pixel intensities\n"
          "\tuse case: --mean [image_path]\n"
          "\t\tMean calculates average pixel value in the image.\n"
          "\n"
          "--cvariance: calculates the range of pixel values\n"
          "\tuse case: --cvariance [image_path]\n"
          "\t\tVariance measures the spread or dispersion of pixel values in the image.\n"
          "\t\tThe higher variance, the wider range of pixel values.\n"
          "\n"
          "--cstdev: calculates the standard deviation of variability in pixel values\n"
          "\tuse case: --cstdev [image_path]\n"
          "\t\tStandard deviation provides a measure of how much pixel values deviate from the mean.\n"
          "\t\tThe higher standard deviation, the greater variability in pixel values.\n"
          "\n"
          "--cvarcoi\n"
          "\tuse case: --cvarcoi [image_path]\n"
          "\t\tVariance coefficient is a measure of relative variability.\n"
          "\t\tIt  provides a relative measure of the spread of pixel values compared to the mean.\n"
          "\n"
          "--casyco: measures the asymmetry of the pixel value distribution\n"
          "\tuse case: --casyco [image_path]\n"
          "\t\tPositive value means the distribution is skewed to the right and negative indicates skewing to the left.\n"
          "\n"
          "--: measures the shape of the pixel value distribution\n"
          "\tuse case: -- [image_path]\n"
          "\t\tThe higher positive coefficient, the sharper peak (more outliers).\n"
          "\t\tNegative coefficient indicates a flatter peak (fewer outliers).\n"
          "\n"
          "--cvarcoii:\n"
          "\tuse case: --cvarcoii [image_path]\n"
          "\n"
          "--centropy: measures the amount of information contained in an image\n"
          "\tuse case: --centropy [image_path]\n"
          "\t\tIt quantifies the randomness or uncertainty of pixel values.\n"
          "\t\tHigher entropy values indicate more complex and diverse pixel distributions.\n"
          "\n"
          "--sedgesharp: enhance the perceived sharpness of edges in an image\n"
          "\tuse case: --sedgesharp [first_image_path] [kernel_size] [output_image_path]\n"
          "\t\t A larger kernel size will result in a stronger sharpening effect\n"
          ""
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
elif sys.argv[1] == "--uhistogram":
    if len(sys.argv) < 6:
        print("Please provide a correct number of parameters.")
    else:
        spatial_filters.uniform_histogram(Image.open(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
elif sys.argv[1] == "--mean":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.mean_pixel_value(Image.open(sys.argv[2])))
elif sys.argv[1] == "--cvariance":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.variance(Image.open(sys.argv[2])))
elif sys.argv[1] == "--cstdev":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.standard_deviation(Image.open(sys.argv[2])))
elif sys.argv[1] == "--cvarcoi":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.variation_coefficient_i(Image.open(sys.argv[2])))
elif sys.argv[1] == "--casyco":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.asymmetry_coefficient(Image.open(sys.argv[2])))
elif sys.argv[1] == "--":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.flattening_coefficient(Image.open(sys.argv[2])))
elif sys.argv[1] == "--cvarcoii":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.variation_coefficient_ii(Image.open(sys.argv[2])))
elif sys.argv[1] == "--centropy":
    if len(sys.argv) != 3:
        print("Please provide a correct number of parameters.")
    else:
        print(characteristics.information_source_entropy(Image.open(sys.argv[2])))
elif sys.argv[1] == "--sedgesharp":
    if len(sys.argv) != 5:
        print("Please provide a correct number of parameters.")
    else:
        print(spatial_filters.edge_sharpening(Image.open(sys.argv[2]), int(sys.argv[3]), sys.argv[4]))
elif sys.argv[1] == "--help":
    if len(sys.argv) != 2:
        print("Unexpected argument for --help.")
    else:
        show_help()
else:
    print("This command does not exist")
