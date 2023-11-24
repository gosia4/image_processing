import support_functions as sp

from PIL import Image


def dilation(image, output = None):
    width, height = image.size
    result_image = Image.new('1', (width, height))

    mask1 = [[1, 1]]
    mask_x_origin = mask1[0]
    mask2 = [[1], [1]]
    mask3 = [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]]

    for x in range(width):
        for y in range(height):
            # pixel = image.getpixel((x, y))
            # sample_arr = []
            for i in range(len(mask3)):
                for j in range(len(mask3[0])):
                    result_x = x + i # albo result_x = x + i -1
                    result_y = y + j
                    if 0 <= result_x < width - 2 and 0 <= result_y < height - 2:
                        pixel = image.getpixel((result_x, result_y))
                        # if sample_arr[i][j] == 1:
                        if pixel == 255:
                            result_image.putpixel((x + 2, y + 2), 255)  # tutaj, żeby ten pixel origin zmienić a nie każdy
                        # else:
                        #     result_image.putpixel((result_x, result_y), pixel)

                            break

            #     else:
            #         continue  # Ten fragment zostanie wykonany, jeśli nie doszło do przerwania wewnętrznej pętli
            #     break  # Przerwij drugą pętlę (ta bez etykiety 'break')
            # else:
            #     continue  # Ten fragment zostanie wykonany, jeśli nie doszło do przerwania zewnętrznej pętli
            # break  # Przerwij trzecią pętlę (ta bez etykiety 'break')

            # for i in range(len(mask1)):
            #     for j in range(1):
            #         # if pixel == 1:
            #         # if sample_arr[i][j] == 1:
            #             # pixel = mask_x_origin
            #         result_x = x + i
            #         result_y = y + j
            #         if 0 <= result_x < width and 0 <= result_y < height:
            #             # if pixel == 1:
            #             if image(result_x, result_y) == 1:
            #             # if image[result_x][result_y] == 1:
            #                 result_image.putpixel((result_x, result_y), 1)
            #             else:
            #                 result_image.putpixel((result_x, result_y), pixel)
            #         # result_image.putpixel((x, y), mask_x_origin)
    result_image.show()
