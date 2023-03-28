from PIL import Image
import numpy as np

def aperture_to_array(pixels, x, y):
    # (x, y) represents the top left corner of the window, where (0, 0) is at the top left of the image
    arr = [[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]]
    for shift_x in range(3):
        for shift_y in range(3):
            arr[shift_x][shift_y] = int(pixels[x + shift_x, y + shift_y] / 255)
    return arr


def erase_isolated_pixels(image):

    new_image = image.copy()
    pixels = new_image.load()
    B1 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    B2 = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    for h in range(image.size[0] - 2):
        for w in range(image.size[1] - 2):
            arr = aperture_to_array(pixels, h, w)
            if np.array_equal(B1, arr):
                pixels[h + 1, w + 1] = (0)
            elif np.array_equal(B2, arr):
                pixels[h + 1, w + 1] = (1)
    return new_image


def erase_edge_pixels(image):

    edge_cases = np.array([[[0, 0, 0],
                   [0, 1, 0],
                   [1, 0, 0]],

                  [[0, 0, 0],
                   [0, 1, 0],
                   [0, 1, 0]],

                  [[0, 0, 0],
                   [0, 1, 0],
                   [1, 1, 0]],

                  [[0, 0, 0],
                   [0, 1, 0],
                   [0, 1, 1]],

                  [[0, 0, 0],
                   [0, 1, 0],
                   [1, 1, 1]]])

    all_edge_cases = edge_cases
    for arr in edge_cases:
        for rotated in range(1, 3):
            np.append(all_edge_cases, np.array([np.rot90(arr, rotated)]), 0)

    all_edge_cases_inversed = 1 - all_edge_cases


    new_image = image.copy()
    pixels = new_image.load()
    for x in range((image.size[0] - 2)):
        for y in range((image.size[1] - 2)):
            ape_arr = aperture_to_array(pixels, x, y)
            flag = False
            for arr in all_edge_cases:
                if np.array_equal(ape_arr, arr):
                    pixels[x + 1, y + 1] = 0
                    flag = True
                    break
            if not flag:
                for arr in all_edge_cases_inversed:
                    if np.array_equal(ape_arr, arr):
                        pixels[x + 1, y + 1] = 1
                        break;

    return new_image


def erase_fringe(image):
    return erase_edge_pixels(erase_isolated_pixels(image))

def difference_image(image1, image2):
    assert image1.size == image2.size
    pixels1 = image1.load()
    pixels2 = image2.load()
    res = Image.new('1', image1.size)
    pixels = res.load()
    for x in range(image1.size[0]):
        for y in range(image1.size[1]):
            pixels[x, y] = abs(pixels1[x, y] - pixels2[x, y])
    return res

if __name__ == '__main__':
    # for imgn in range(1, 6):
    #     with Image.open(f'./src/binary{imgn}.bmp').convert('1') as img:
    #         tmp1 = erase_fringe(img)
    #         tmp2 = erase_fringe(tmp1)
    #         tmp1.save(f'./out/filtered{imgn}.bmp')
    #         print(f'Image #{imgn} done')

    # with Image.open(f'./src/binary1.bmp').convert('1') as img:
    #     tmp = erase_fringe(img)
    #     i = 0
    #     while(i<6):
    #         i+=1
    #         tmp1 = erase_fringe(tmp)
    #         tmp = tmp1
    #         print(f'pass {i}')
    #
    #     tmp.save(f'./out/filtered1_6_passes.bmp')

    # i1 = Image.open(f'./src/binary6.png').convert('1')
    # i2 = Image.open(f'./out/filtered6_6_passes.bmp').convert('1')
    #
    # difference_image(i1, i2).save(f'./out/diff6.bmp')
