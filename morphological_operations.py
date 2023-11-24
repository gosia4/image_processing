import support_functions as sp

from PIL import Image
import numpy as np


def dilation(image, output, show=True):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    one_bit_image_array = np.transpose(np.array(image))

    white_pixel_found = False

    for x in range(width):
        for y in range(height):

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if one_bit_image_array[target_x][target_y]:
                            result_image.putpixel((x, y), 1)
                            white_pixel_found = True
                            break
                if white_pixel_found:
                    white_pixel_found = False
                    break

    if show:
        result_image.show()
    #result_image.save(output)
    return result_image


def erosion(image, output, show=True):
    width, height = image.size
    result_image = Image.new('1', (width, height), 1)
    one_bit_image_array = np.transpose(np.array(image))

    black_pixel_found = False

    for x in range(width):
        for y in range(height):

            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if one_bit_image_array[target_x][target_y] == 0:
                            result_image.putpixel((x, y), 0)
                            black_pixel_found = True
                            break
                if black_pixel_found:
                    black_pixel_found = False
                    break

    if show:
        result_image.show()
    #result_image.save(output)
    return result_image


def opening(image, output):
    width, height = image.size
    dilation_image = dilation(image, None, False)
    result_image = erosion(dilation_image, None, False)
    result_image.show()
    #result_image.save(output)


def closing(image, output):
    width, height = image.size
    erosion_image = erosion(image, None, False)
    result_image = dilation(erosion_image, None, False)
    #result_image.save(output)
    result_image.show()


def hmt_transformation(image, output):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    one_bit_image_array = np.transpose(np.array(image))

    for x in range(width-2):
        for y in range(height-2):
            sample_arr = []
            if (one_bit_image_array[x][y] and one_bit_image_array[x][y + 1] and one_bit_image_array[x][y + 2]) == 1:
                if one_bit_image_array[x + 1][y + 1] == 0:
                    result_image.putpixel((x + 1, y + 1), 1)
    result_image.show()
    sp.save_image(result_image, output)


def hmt_transformation_xi1(image, output):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    one_bit_image_array = np.transpose(np.array(image))

    for x in range(1, width-1):
        for y in range(1, height-1):
            match = True
            if one_bit_image_array[x][y] == 0:
                for i in range(-1, 2):
                    if one_bit_image_array[x-1][y + i] == 0:
                        match = False
                        break
                if match:
                    result_image.putpixel((x, y), 1)

    result_image.show()
    sp.save_image(result_image, output)


def hmt_transformation_general(image, mask, output):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    one_bit_image_array = np.transpose(np.array(image))
    mask = np.transpose(mask)

    for x in range(1, width-1):
        for y in range(1, height-1):
            matching = True
            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if mask[i+1][j+1] == 2:
                            continue
                        if one_bit_image_array[target_x][target_y] != mask[i+1][j+1]:
                            matching = False
                            break
                if matching == False:
                    break
            if matching:
                result_image.putpixel((x,y), 1)

    result_image.show()
    sp.save_image(result_image, output)

def region_growing(image, chosen_x, chosen_y, treshold, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]
    result_image.putpixel((chosen_x,chosen_y), 255)

    while True:
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 255:

                        if (image_array[region[a][0]][region[a][1]] - treshold <=
                                image_array[region[a][0] + i][region[a][1] + j] <=
                                image_array[region[a][0]][region[a][1]] + treshold):

                            region.append([region[a][0] + i, region[a][1] + j])
                            result_image.putpixel((region[a][0] + i, region[a][1] + j), 255)

            region.pop(0)
        break
    result_image.show()
    sp.save_image(result_image, output)


def region_growing_2(image, chosen_x, chosen_y, treshold, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]
    result_image.putpixel((chosen_x, chosen_y), 255)
    iteratons = 0
    while True:
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 255:

                        min_val = image_array[region[a][0]][region[a][1]] - treshold
                        max_val = image_array[region[a][0]][region[a][1]] + treshold
                        checking_value = image_array[region[a][0] + i][region[a][1] + j]

                        if ( min_val <= checking_value <= max_val):
                            region.append([region[a][0] + i, region[a][1] + j])
                            # print(region)
                            result_image.putpixel((region[a][0] + i, region[a][1] + j), 255)

            # nuber of regions have changed +x and the -1 this will sometimes cause a index oft of range

            region.pop(0)
            iteratons += 1
            print(iteratons)
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)

