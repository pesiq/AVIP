from PIL import Image
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
# from os import path
from math import pow, log, log2, floor

def semitone(img):
    return (0.3 * img[:, :, 0] + 0.59 * img[:, :, 1] + 0.11 *
            img[:, :, 2]).astype(np.uint8)


# def to_semitone(img_name):
#     img = image_to_np_array(img_name)
#     return Image.fromarray(semitone(img), 'L')

def contrast(img: np.array):
    flat_img = img.flatten()
    mn = round(mean(flat_img))

    positiveRange = max(2, max(flat_img) - mn)
    negativeRange = max(2, mn - min(flat_img))

    positiveAlpha = 2 ** 7 / log(positiveRange)
    negativeAlpha = 2 ** 7 / log(negativeRange)

    res_img = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            f = img[i, j] - mn
            if f >= 1:
                res_img[i, j] = mn + positiveAlpha * log(f)
            elif f <= -1:
                res_img[i, j] = mn - negativeAlpha * log(abs(f))
            else:
                res_img[i, j] = mn

    return res_img

def haralik(img_arr: np.array, d = 2):
    matrix = np.zeros(shape=(256, 256))

    for x in range(d, img_arr.shape[0] - d):
        for y in range(d, img_arr.shape[1] - d):
            matrix[img_arr[x - d, y], img_arr[x, y]] += 1
            matrix[img_arr[x + d, y], img_arr[x, y]] += 1
            matrix[img_arr[x, y - d], img_arr[x, y]] += 1
            matrix[img_arr[x, y + d], img_arr[x, y]] += 1

    for x in range(256):
        m = np.array(matrix[x])
        m[np.where(m == 0)] = 1
        matrix[x] = np.log(m)
    matrix = matrix * 256 / np.max(matrix)
    return matrix


def CON(har: np.array):
    sum = 0
    for i in range(har.shape[0]):
        for j in range(har.shape[1]):
            sum += (i - j) ** 2 * har[i, j]

    return sum


def LUN(har: np.array):
    sum = 0
    for i in range(har.shape[0]):
        for j in range(har.shape[1]):
            sum += har[i, j] / (1 + (i - j) ** 2)

    return sum


if __name__ == '__main__':


    name = f'brick'

    with Image.open(f'./source/{name}.png').convert() as image:
        semi = semitone(np.array(image))

        trans = contrast(semi)

        contrasted = contrast(semi)
        imgc = Image.fromarray(contrasted.astype(np.uint8), 'L')
        imgc.save(f'./result/{name}_contrasted.png')

        figure, axis = plt.subplots(2, 1)
        axis[0].hist(x=semi.flatten(), bins=np.arange(0, 255))
        axis[0].title.set_text('Origianl')

        axis[1].hist(x=trans.flatten(), bins=np.arange(0, 255))
        axis[1].title.set_text('Transformed')
        plt.tight_layout()
        plt.savefig(f'./result/{name}_histogram.png')

        matrix = haralik(semi.astype(np.uint8))
        result = Image.fromarray(matrix.astype(np.uint8), "L")
        result.save(f'./result/{name}_hiralik.png')

        t_matrix = haralik(trans.astype(np.uint8))
        t_result = Image.fromarray(t_matrix.astype(np.uint8), "L")
        t_result.save(f'./result/{name}_HC.png')

        print(f"CON: {CON(matrix)}")
        print(f"CON (contrasted): {CON(t_matrix)}")

        print(f"LUN: {LUN(matrix)}")
        print(f"LUN (contrasted): {LUN(t_matrix)}")

    # transformed = contrast(semi)
    # transformed_img = Image.fromarray(transformed.astype(np.uint8), "L")
    # transformed_img.save(path.join('profile', 'contrasted', selected_image))
    #
    # figure, axis = plt.subplots(2, 1)
    # axis[0].hist(x=semi.flatten(), bins=np.arange(0, 255))
    # axis[0].title.set_text('Исходное изображение')
    #
    # axis[1].hist(x=transformed.flatten(), bins=np.arange(0, 255))
    # axis[1].title.set_text('Преобразованное изображение')
    # plt.tight_layout()
    # plt.savefig(path.join('profile', 'histograms', selected_image))
    #
    # matrix = haralik(semi.astype(np.uint8))
    # result = Image.fromarray(matrix.astype(np.uint8), "L")
    # result.save(path.join('profile', 'haralik', selected_image))
    #
    # t_matrix = haralik(transformed.astype(np.uint8))
    # t_result = Image.fromarray(t_matrix.astype(np.uint8), "L")
    # t_result.save(path.join('profile', 'haralik_contrasted', selected_image))
    #
    # print(f"CON: {CON(matrix)}")
    # print(f"CON (contrasted): {CON(t_matrix)}")
    #
    # print(f"LUN: {LUN(matrix)}")
    # print(f"LUN (contrasted): {LUN(t_matrix)}")
