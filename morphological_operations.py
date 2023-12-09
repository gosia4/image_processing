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
    result_image.save(output)
    return result_image


def dilation_with_mask(image, mask, output, show=True):
    masks = [
        np.array([[1, 1]]),  # Mask 1
        np.array([[1], [1]]),  # Mask 2
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),  # Mask 3
        np.array([[2, 1, 2], [1, 1, 1], [2, 1, 2]])  # Mask 4
    ]
    if isinstance(mask, int):
        selected_mask = np.transpose(masks[mask - 1])  # to be sure that the right mask is chosen
    else:
        selected_mask = np.transpose(mask)

    width, height = image.size
    result_image = Image.new('1', (width, height))
    one_bit_image_array = np.array(image)

    for x in range(width):
        for y in range(height):
            max_pixel_value = 0 # if the surrounding pixel and the origin is 1, then it is set to one

            struct_width, struct_height = selected_mask.shape
            for i in range(struct_width):
                for j in range(struct_height):
                    target_x = x + i - (struct_width // 2)
                    target_y = y + j - (struct_height // 2)

                    if 0 <= target_x < width and 0 <= target_y < height:
                        if selected_mask[i, j] == 1 and one_bit_image_array[target_y, target_x] == 1: # odwrotnie działa
                            max_pixel_value = 1
                            break

                if max_pixel_value == 1:
                    break

            result_image.putpixel((x, y), max_pixel_value)

    if show:
        result_image.show()
    if output is not None:
        sp.save_image(result_image, output)
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
    result_image.save(output)
    return result_image


def erosion_with_mask(image, mask, output, show=True):
    masks = [
        np.array([[1, 1]]),  # Mask 1
        np.array([[1], [1]]),  # Mask 2
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),  # Mask 3
        np.array([[2, 1, 2], [1, 1, 1], [2, 1, 2]])  # Mask 4
    ]

    if isinstance(mask, int):
        selected_mask = np.transpose(masks[mask - 1])  # to be sure that the right mask is chosen
    else:
        selected_mask = np.transpose(mask)

    width, height = image.size
    result_image = Image.new('1', (width, height), 1)
    one_bit_image_array = np.transpose(np.array(image))

    for x in range(width):
        for y in range(height):

            max_pixel_value = 1  # if the surrounding pixel and the origin is 1, then it is set to one

            struct_width, struct_height = selected_mask.shape

            for i in range(struct_width):
                for j in range(struct_height):
                    target_x = x + i - (struct_width // 2)
                    target_y = y + j - (struct_height // 2)
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if one_bit_image_array[target_x][target_y] == 0:
                            result_image.putpixel((x, y), 0)
                            max_pixel_value = 0
                            break

                if max_pixel_value == 0:
                    break

            result_image.putpixel((x, y), max_pixel_value)

    if show:
        result_image.show()
    if output is not None:
        sp.save_image(result_image, output)
    return result_image


def opening(image, mask, output):
    width, height = image.size
    # erosion_image = erosion(image, None, False)
    # result_image = dilation(erosion_image, None, False)
    erosion_image = erosion_with_mask(image, mask, None, False)
    result_image = dilation_with_mask(erosion_image, mask, None, False)
    sp.save_image(result_image, output)
    result_image.show()


def closing(image, mask, output):
    width, height = image.size
    # dilation_image = dilation(image, None, False)
    # result_image = erosion(dilation_image, None, False)
    dilated_image = dilation_with_mask(image, mask, None, False)
    result_image = erosion_with_mask(dilated_image, mask, None, False)
    result_image.show()
    sp.save_image(result_image, output)


def hmt_transformation_xi(image, output):
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
    masks = [
        np.array([[1, 1, 1], [2, 0, 2], [0, 0, 0]]),  # Mask XII 1
        np.array([[0, 0, 0], [2, 1, 2], [2, 2, 2]]),  # Mask XI 2
        np.array([[2, 2, 0], [2,1, 0], [2, 2, 0]]),  # Mask XI 3
        np.array([[1, 1, 2], [1, 0, 0], [2, 0, 0]])  # Mask XII 8
    ]
    if isinstance(mask, int):
        selected_mask = np.transpose(masks[mask - 1])  # to be sure that the right mask is chosen
    else:
        selected_mask = np.transpose(mask)

    for x in range(1, width-1):
        for y in range(1, height-1):
            matching = True
            for i in range(-1, 2):
                for j in range(-1, 2):
                    target_x = x + i
                    target_y = y + j
                    if 0 <= target_x < width - 1 and 0 <= target_y < height - 1:
                        if selected_mask[i+1][j+1] == 2:
                            continue
                        if one_bit_image_array[target_x][target_y] != selected_mask[i+1][j+1]:
                            matching = False
                            break
                if matching == False:
                    break
            if matching:
                result_image.putpixel((x,y), 1)

    result_image.show()
    sp.save_image(result_image, output)

def region_growing_static(image, chosen_x, chosen_y, treshold, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]
    min_val = image_array[chosen_x][chosen_y] - treshold
    max_val = image_array[chosen_x][chosen_y] + treshold

    # each new added region pixel will be stored here (pixel in the new_region list are the ones on the edges of the region)
    new_region = []

    result_image.putpixel((chosen_x, chosen_y), 255)
    while True: # while region still has some new members to investigate: repeat
        # investigate each and every member of the current region
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 255 and 0 <= region[a][0] + i < width - 1 and 0 <= region[a][1] + j < height - 1:

                        potential_region_member = image_array[region[a][0] + i][region[a][1] + j]
                        # minimal and maximal values are based on the originally chosen pixel
                        if (min_val <= potential_region_member <= max_val):
                            new_region.append([region[a][0] + i, region[a][1] + j])
                            result_image.putpixel((region[a][0] + i, region[a][1] + j), 255)

        # all region members are dropped and exchanged for the new_region members (which are located on the edges of the region)
        # while growing the region does not need to consider pixels already deep inside the region
        region = new_region
        new_region = []
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)
    return result_image

def region_growing_static_with_image_background(image, chosen_x, chosen_y, treshold, output):
    width, height = image.size
    result_image = image.copy()
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]
    min_val = image_array[chosen_x][chosen_y] - treshold
    max_val = image_array[chosen_x][chosen_y] + treshold

    # each new added region pixel will be stored here (pixel in the new_region list are the ones on the edges of the region)
    new_region = []

    result_image.putpixel((chosen_x, chosen_y), 255)
    while True: # while region still has some new members to investigate: repeat
        # investigate each and every member of the current region
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 255 and 0 <= region[a][0] + i < width - 1 and 0 <= region[a][1] + j < height - 1:

                        potential_region_member = image_array[region[a][0] + i][region[a][1] + j]
                        # minimal and maximal values are based on the originally chosen pixel
                        if (min_val <= potential_region_member <= max_val):
                            new_region.append([region[a][0] + i, region[a][1] + j])
                            result_image.putpixel((region[a][0] + i, region[a][1] + j), 255)

        # all region members are dropped and exchanged for the new_region members (which are located on the edges of the region)
        # while growing the region does not need to consider pixels already deep inside the region
        region = new_region
        new_region = []
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)
    return result_image


# contagious region growing works by changing the targeted pixel value for each member whose neighbourhood
# we are currently investigating with min and max as: investigating pixel - threshold and investigating pixel + threshold
def region_growing_contagious(image, chosen_x, chosen_y, treshold, output):
    width, height = image.size
    result_image, color_channels = sp.analyse_color_channels(image)
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]

    # each new added region pixel will be stored here (pixel in the new_region list are the ones on the edges of the region)
    new_region = []

    result_image.putpixel((chosen_x, chosen_y), 255)
    while True: # while region still has some new members to investigate: repeat
        # investigate each and every member of the current region
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 255 and 0 <= region[a][0] + i < width - 1 and 0 <= region[a][1] + j < height - 1:

                        # minimal and maximal values are based on the value image_array[region[a][0]][region[a][1]] which is the pixel from the region that we are currently investigating
                        min_val = image_array[region[a][0]][region[a][1]] - treshold
                        max_val = image_array[region[a][0]][region[a][1]] + treshold
                        potential_region_member = image_array[region[a][0] + i][region[a][1] + j]

                        if ( min_val <= potential_region_member <= max_val):
                            new_region.append([region[a][0] + i, region[a][1] + j])
                            result_image.putpixel((region[a][0] + i, region[a][1] + j), 255)

        # all region members are dropped and exchanged for the new_region members (which are located on the edges of the region)
        # while growing the region does not need to consider pixels already deep inside the region
        region = new_region
        new_region = []
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)

def region_growing_contagious_with_image_background(image, chosen_x, chosen_y, treshold, output):
    width, height = image.size
    result_image = image.copy()
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]

    # each new added region pixel will be stored here (pixel in the new_region list are the ones on the edges of the region)
    new_region = []

    result_image.putpixel((chosen_x, chosen_y), 255)
    while True: # while region still has some new members to investigate: repeat
        # investigate each and every member of the current region
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 255 and 0 <= region[a][0] + i < width - 1 and 0 <= region[a][1] + j < height - 1:

                        # minimal and maximal values are based on the value image_array[region[a][0]][region[a][1]] which is the pixel from the region that we are currently investigating
                        min_val = image_array[region[a][0]][region[a][1]] - treshold
                        max_val = image_array[region[a][0]][region[a][1]] + treshold
                        potential_region_member = image_array[region[a][0] + i][region[a][1] + j]

                        if ( min_val <= potential_region_member <= max_val):
                            new_region.append([region[a][0] + i, region[a][1] + j])
                            result_image.putpixel((region[a][0] + i, region[a][1] + j), 255)

        # all region members are dropped and exchanged for the new_region members (which are located on the edges of the region)
        # while growing the region does not need to consider pixels already deep inside the region
        region = new_region
        new_region = []
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)


def intersection(image1, image2):
    width, height = image1.size
    result_image = Image.new('1', (width, height))

    for i in range(width):
        for j in range(height):
            pixel1 = image1.getpixel((i, j))
            pixel2 = image2.getpixel((i, j))

            # print(f"Pixel1: {pixel1}, Pixel2: {pixel2}")

            if pixel1 == 1 and pixel2 == 1:
                result_image.putpixel((i, j), 1)
            else:
                result_image.putpixel((i, j), 0)

    return result_image


def m3_region(image, chosen_x, chosen_y, mask_no, output):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    image_array = np.transpose(np.array(image))

    region = [[chosen_x, chosen_y]]

    masks = {
        1: np.array([[1, 1, 1],
                     [1, 1, 1],
                     [1, 1, 1]]),
        2: np.array([[2, 1, 2],
                     [1, 1, 1],
                     [2, 1, 2]])
    }

    mask = masks[mask_no]

    # each new added region pixel will be stored here (pixel in the new_region list are the ones on the edges of the region)
    new_region = []

    result_image.putpixel((chosen_x, chosen_y), 1)
    while True:  # while region still has some new members to investigate: repeat
        # investigate each and every member of the current region
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 1 and 0 <= region[a][
                        0] + i < width - 1 and 0 <= region[a][1] + j < height - 1:
                        if mask[i + 1][j + 1] == 1:
                            potential_region_member = image_array[region[a][0] + i][region[a][1] + j]
                            # minimal and maximal values are based on the originally chosen pixel
                            if (image.getpixel((region[a][0] + i, region[a][1] + j))):
                                new_region.append([region[a][0] + i, region[a][1] + j])
                                result_image.putpixel((region[a][0] + i, region[a][1] + j), 1)

        # all region members are dropped and exchanged for the new_region members (which are located on the edges of the region)
        # while growing the region does not need to consider pixels already deep inside the region
        region = new_region
        new_region = []
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)
    return result_image

def m3_region_flexible(image, chosen_x, chosen_y, mask, output):
    width, height = image.size
    result_image = Image.new('1', (width, height))
    image_array = np.transpose(np.array(image))

    pixel_color = image_array[chosen_x][chosen_y]
    region = [[chosen_x, chosen_y]]

    masks = {
        1: np.array([[1, 1, 1],
                     [1, 1, 1],
                     [1, 1, 1]]),
        2: np.array([[2, 1, 2],
                     [1, 1, 1],
                     [2, 1, 2]])
    }

    if isinstance(mask, int):
        selected_mask = np.transpose(masks[mask - 1])  # to be sure that the right mask is chosen
    else:
        selected_mask = np.transpose(mask)

    # each new added region pixel will be stored here (pixel in the new_region list are the ones on the edges of the region)
    new_region = []

    result_image.putpixel((chosen_x, chosen_y), 1)
    while True:  # while region still has some new members to investigate: repeat
        # investigate each and every member of the current region
        for a in range(len(region)):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if result_image.getpixel((region[a][0] + i, region[a][1] + j)) != 1 and 0 <= region[a][
                        0] + i < width - 1 and 0 <= region[a][1] + j < height - 1:
                        if selected_mask[i+1][j+1] == 1:

                            potential_region_member = image_array[region[a][0] + i][region[a][1] + j]
                            # minimal and maximal values are based on the originally chosen pixel
                            if (image_array[region[a][0] + i][region[a][1] + j] == pixel_color):
                                new_region.append([region[a][0] + i, region[a][1] + j])
                                result_image.putpixel((region[a][0] + i, region[a][1] + j), 1)


        # all region members are dropped and exchanged for the new_region members (which are located on the edges of the region)
        # while growing the region does not need to consider pixels already deep inside the region
        region = new_region
        new_region = []
        if (len(region) == 0):
            break
    result_image.show()
    sp.save_image(result_image, output)
    return result_image