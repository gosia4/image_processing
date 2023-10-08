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
if len(new_x) < 1 or len(new_x) > 2:
    print("Error, provide correct numbers of arguments")
else:
    if new_x[0] == "--brightness":
        if len(new_x) != 2:
            print("Error, provide correct numbers of parameter")
        else:
            basic_operations.modify_brightness2(im, int(new_x[1]))
    elif new_x[0] == "--contrast":
        if len(new_x) != 2:
            print("Error, provide correct numbers of parameter")
        else:
            basic_operations.modify_contrast3(im, int(new_x[1]))
    elif new_x[0] == "--negative":
        basic_operations.apply_negative(im)
    elif new_x[0] == "--hflip":
        geometric_operations.horizontal_flip(im)
    elif new_x[0] == "--vflip":
        geometric_operations.vertical_flip(im)
    elif new_x[0] == "--dflip":
        geometric_operations.diagonal_flip(im)
    elif new_x[0] == "--shrink":
        if len(new_x) != 2:
            print("Error, provide correct numbers of parameter")
        else:
            geometric_operations.shrinking(im, new_x[1])
    # elif new_x[0] == "--enlarge":
    #     if len(new_x) != 2:
    #         print("Error, provide correct numbers of parameter")
    #     else:
    #         geometric_operations.enlarge(im, new_x[1])
    elif new_x[0] == "--help":
        show_help()
    else:
        print("This command does not exist")

# example
# geometric_operations.vertical_flip(im)
# show_help()
